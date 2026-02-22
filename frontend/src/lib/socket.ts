import { WSMessage } from '@/types/scan';

export function connectToScan(
    scanId: string,
    onMessage: (msg: WSMessage) => void,
    onClose: () => void
): () => void {
    const wsURL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';
    let ws: WebSocket | null = null;
    let reconnectAttempts = 0;
    const MAX_RECONNECT = 3;
    let isIntentionallyClosed = false;

    const connect = () => {
        ws = new WebSocket(`${wsURL}/ws/scan/${scanId}`);

        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                onMessage(msg);
            } catch (e) {
                console.error('Failed to parse WS message', e, event.data);
            }
        };

        ws.onclose = () => {
            if (!isIntentionallyClosed && reconnectAttempts < MAX_RECONNECT) {
                reconnectAttempts++;
                setTimeout(connect, Math.min(1000 * Math.pow(2, reconnectAttempts), 10000));
            } else if (!isIntentionallyClosed) {
                onClose();
            }
        };

        ws.onerror = () => {
            // close event will handle reconnect
            ws?.close();
        };
    };

    connect();

    return () => {
        isIntentionallyClosed = true;
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.close();
        }
    };
}
