export type ConnectionStatus = 'LIVE' | 'RECONNECTING' | 'OFFLINE';

export type WebSocketEventHandler = (data: any) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private statusListeners: Set<(status: ConnectionStatus) => void> = new Set();
  private eventListeners: Map<string, Set<WebSocketEventHandler>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectTimer: any = null;
  private isExplicitlyClosed = false;
  private currentStatus: ConnectionStatus = 'OFFLINE';

  constructor() {
    // Connect via Vite proxy or fallback directly to 8000
    const isHttps = window.location.protocol === 'https:';
    const host = window.location.hostname;
    // Connect to port 8000 directly or via proxy
    this.url = `${isHttps ? 'wss:' : 'ws:'}//${host}:8000/ws/live`;
  }

  public connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    this.isExplicitlyClosed = false;
    this.setStatus('RECONNECTING');

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.reconnectAttempts = 0;
        this.setStatus('LIVE');
        console.log('[FRAUD-X WS] Connection established to real-time stream hub.');
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          const { type, data } = message;
          if (type && this.eventListeners.has(type)) {
            const handlers = this.eventListeners.get(type)!;
            handlers.forEach(fn => fn(data));
          }
        } catch (err) {
          console.warn('[FRAUD-X WS] Error parsing incoming event:', err);
        }
      };

      this.ws.onclose = (event) => {
        if (!this.isExplicitlyClosed) {
          this.setStatus('OFFLINE');
          this.scheduleReconnect();
        }
      };

      this.ws.onerror = (err) => {
        console.warn('[FRAUD-X WS] Socket error encountered:', err);
        this.setStatus('OFFLINE');
      };
    } catch (e) {
      this.setStatus('OFFLINE');
      this.scheduleReconnect();
    }
  }

  private scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts || this.isExplicitlyClosed) {
      return;
    }

    const backoff = Math.min(10000, 1000 * Math.pow(1.5, this.reconnectAttempts));
    this.reconnectAttempts++;
    this.setStatus('RECONNECTING');

    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.reconnectTimer = setTimeout(() => {
      this.connect();
    }, backoff);
  }

  public onStatusChange(callback: (status: ConnectionStatus) => void): () => void {
    this.statusListeners.add(callback);
    callback(this.currentStatus);
    return () => {
      this.statusListeners.delete(callback);
    };
  }

  public on(eventType: string, handler: WebSocketEventHandler): () => void {
    if (!this.eventListeners.has(eventType)) {
      this.eventListeners.set(eventType, new Set());
    }
    this.eventListeners.get(eventType)!.add(handler);

    return () => {
      const handlers = this.eventListeners.get(eventType);
      if (handlers) {
        handlers.delete(handler);
        if (handlers.size === 0) {
          this.eventListeners.delete(eventType);
        }
      }
    };
  }

  public disconnect() {
    this.isExplicitlyClosed = true;
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.setStatus('OFFLINE');
  }

  private setStatus(status: ConnectionStatus) {
    this.currentStatus = status;
    this.statusListeners.forEach(fn => fn(status));
  }

  public getStatus(): ConnectionStatus {
    return this.currentStatus;
  }
}

export const wsService = new WebSocketClient();
