import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import os

class VideoColorAnalysisSystem:
    def __init__(self):
        # Initialize webcam input
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Cannot open webcam")

        # Get video parameters
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps == 0 or np.isnan(self.fps):
            self.fps = 30  # default FPS
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Initialize ROI (region of interest) parameters
        self.ROI_WIDTH = 50
        self.ROI_HEIGHT = 50
        self.roi_top_left = [100, 100]
        self.dragging = False

        # Optional HSV mask range for blue detection
        self.lower_blue = np.array([90, 50, 50])
        self.upper_blue = np.array([130, 255, 255])

        # Storage for time and RGB data
        self.time_data = []
        self.rgb_data = {'R': [], 'G': [], 'B': []}
        self.start_time = time.time()

        # Setup output directory and CSV file for data logging
        self.output_dir = "analysis_results"
        os.makedirs(self.output_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.data_file = open(os.path.join(self.output_dir, f"rgb_data_{timestamp}.csv"), "w")
        self.data_file.write("Time(s),Red,Green,Blue\n")

        # Setup GUI windows and plotting figure
        self.setup_visualization()
        cv2.setMouseCallback("Main View", self.mouse_callback)

    def setup_visualization(self):
        """Setup OpenCV windows and Matplotlib figure."""
        cv2.namedWindow("Main View", cv2.WINDOW_NORMAL)
        cv2.namedWindow("ROI View", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Main View", 800, 600)
        cv2.resizeWindow("ROI View", 400, 300)

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.lines = {
            'R': self.ax.plot([], [], 'r-', label='Red')[0],
            'G': self.ax.plot([], [], 'g-', label='Green')[0],
            'B': self.ax.plot([], [], 'b-', label='Blue')[0]
        }
        self.ax.set_title("Real-time RGB Channels Intensity")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Intensity (0-255)")
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 255)
        self.ax.legend()
        self.ax.grid(True)

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events to allow dragging of ROI."""
        if event == cv2.EVENT_LBUTTONDOWN:
            x1, y1 = self.roi_top_left
            x2, y2 = x1 + self.ROI_WIDTH, y1 + self.ROI_HEIGHT
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.dragging = True
                self.mouse_offset = (x - x1, y - y1)

        elif event == cv2.EVENT_MOUSEMOVE and self.dragging:
            dx, dy = self.mouse_offset
            new_x = max(0, min(self.width - self.ROI_WIDTH, x - dx))
            new_y = max(0, min(self.height - self.ROI_HEIGHT, y - dy))
            self.roi_top_left = [new_x, new_y]

        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False

    def process_frame(self, frame):
        """Extract ROI and compute average RGB values. Optional: apply blue mask."""
        x1, y1 = self.roi_top_left
        x2, y2 = x1 + self.ROI_WIDTH, y1 + self.ROI_HEIGHT
        roi = frame[y1:y2, x1:x2]

        # If you want to use a blue color mask in HSV, uncomment below:
        # hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        # masked_roi = cv2.bitwise_and(roi, roi, mask=mask)
        # b, g, r, _ = cv2.mean(roi, mask=mask)

        # Default behavior: compute mean RGB without masking
        b, g, r, _ = cv2.mean(roi)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, f"R:{int(r)} G:{int(g)} B:{int(b)}", (30,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        return frame, roi, (r, g, b)

    def update_visualization(self, frame, roi, rgb_values):
        """Display frames and update RGB plot in real-time."""
        main_display = cv2.resize(frame, (800, 600))
        roi_display = cv2.resize(roi, (400, 300))

        cv2.imshow("Main View", main_display)
        cv2.imshow("ROI View", roi_display)

        current_time = time.time() - self.start_time
        self.time_data.append(current_time)
        for i, channel in enumerate(['R', 'G', 'B']):
            self.rgb_data[channel].append(rgb_values[i])
            self.lines[channel].set_data(self.time_data, self.rgb_data[channel])

        self.ax.set_xlim(0, max(10, current_time))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # Log RGB values to CSV
        self.data_file.write(f"{current_time:.2f},{rgb_values[0]:.1f},{rgb_values[1]:.1f},{rgb_values[2]:.1f}\n")

    def run_analysis(self):
        """Main loop: capture, process, and visualize frames."""
        try:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                processed_frame, roi, rgb = self.process_frame(frame)
                self.update_visualization(processed_frame, roi, rgb)

                if cv2.waitKey(int(1000/self.fps)) & 0xFF == ord('q'):
                    break
        finally:
            self.cleanup()

    def cleanup(self):
        """Release resources and save final plot."""
        self.cap.release()
        self.data_file.close()
        cv2.destroyAllWindows()
        plt.ioff()
        plt.savefig(os.path.join(self.output_dir, "final_rgb_plot.png"), dpi=300)
        print(f"Analysis complete. Results saved in '{self.output_dir}'.")

if __name__ == "__main__":
    analyzer = VideoColorAnalysisSystem()
    analyzer.run_analysis()
