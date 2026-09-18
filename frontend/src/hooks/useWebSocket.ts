import { useState, useEffect } from 'react';
import { wsService, ConnectionStatus } from '../services/websocket';

export function useWebSocket() {
  const [status, setStatus] = useState<ConnectionStatus>(wsService.getStatus());

  useEffect(() => {
    wsService.connect();
    const unsubscribe = wsService.onStatusChange((newStatus) => {
      setStatus(newStatus);
    });

    return () => {
      unsubscribe();
    };
  }, []);

  return { status };
}
