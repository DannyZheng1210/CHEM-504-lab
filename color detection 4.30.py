import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import datetime
import os

class ColourDetection:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.time_list = []
        self.rgb_list = []

        self.ROI_WIDTH = 100
        self.ROI_HEIGHT = 100
        self.roi_top_left = [100, 100]  # Modify this manually as needed
        self.dragging = False

        # Setup output folder
        os.makedirs("colour_detection_values", exist_ok=True)
        os.makedirs("colour_detection_graph", exist_ok=True)

        # Setup plot
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.lines = {
            'R': self.ax.plot([], [], 'r-', label='Red')[0],
            'G': self.ax.plot([], [], 'g-', label='Green')[0],
            'B': self.ax.plot([], [], 'b-', label='Blue')[0]
        }
        self.ax.set_title("RGB Average in ROI")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Intensity")
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 255)
        self.ax.legend()
        self.ax.grid(True)

    def get_timestamp(self):
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x1, y1 = self.roi_top_left
            x2, y2 = x1 + self.ROI_WIDTH, y1 + self.ROI_HEIGHT
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.dragging = True
                self.mouse_offset = (x - x1, y - y1)

        elif event == cv2.EVENT_MOUSEMOVE and self.dragging:
            dx, dy = self.mouse_offset
            new_x = max(0, min(int(self.cap.get(3)) - self.ROI_WIDTH, x - dx))
            new_y = max(0, min(int(self.cap.get(4)) - self.ROI_HEIGHT, y - dy))
            self.roi_top_left = [new_x, new_y]

        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False

    def capture(self):
        start_time = time.time()
        cv2.namedWindow("Color Detection")
        cv2.namedWindow("ROI")
        cv2.setMouseCallback("Color Detection", self.mouse_callback)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            x1, y1 = self.roi_top_left
            x2, y2 = x1 + self.ROI_WIDTH, y1 + self.ROI_HEIGHT
            roi = frame[y1:y2, x1:x2]

            # Calculate mean RGB values of ROI
            b, g, r, _ = cv2.mean(roi)
            elapsed_time = time.time() - start_time
            self.time_list.append(elapsed_time)
            self.rgb_list.append((r, g, b))

            # Draw ROI rectangle and info
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"R:{int(r)} G:{int(g)} B:{int(b)}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, f"ROI Pos: ({x1}, {y1})", (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            cv2.imshow("Color Detection", frame)
            cv2.imshow("ROI", roi)

            # Update plot
            for i, ch in enumerate(['R', 'G', 'B']):
                self.lines[ch].set_data(self.time_list, [v[i] for v in self.rgb_list])

            self.ax.set_xlim(0, max(10, elapsed_time))
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if elapsed_time > 30:
                break

        # Save final frame as image before releasing the camera
        timestamp = self.get_timestamp()
        image_path = f"colour_detection_values/final_frame_{timestamp}.png"
        cv2.imwrite(image_path, frame)

        self.cap.release()
        cv2.destroyAllWindows()
        self.save_to_csv()
        self.save_plot()

    def save_to_csv(self):
        timestamp = self.get_timestamp()
        path = f"colour_detection_values/color_detection_{timestamp}.csv"
        df = pd.DataFrame({
            "Time (s)": self.time_list,
            "Red": [v[0] for v in self.rgb_list],
            "Green": [v[1] for v in self.rgb_list],
            "Blue": [v[2] for v in self.rgb_list],
        })
        df.to_csv(path, index=False)

    def save_plot(self):
        timestamp = self.get_timestamp()
        path = f"colour_detection_graph/Figure_{timestamp}.png"
        plt.ioff()
        plt.savefig(path, dpi=300)

if __name__ == '__main__':
    ColourDetection().capture()
