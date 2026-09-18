/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0b0d11",
        surface: {
          DEFAULT: "#12151c",
          nested: "#171a23",
          hover: "#1c202c",
          border: "rgba(255, 255, 255, 0.08)",
        },
        risk: {
          low: "#10b981",
          medium: "#f59e0b",
          high: "#f97316",
          critical: "#ef4444"
        },
        accent: {
          DEFAULT: "#0284c7", // Restrained enterprise sky/cyan
          muted: "#0369a1",
          light: "#38bdf8",
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif']
      }
    },
  },
  plugins: [],
}
