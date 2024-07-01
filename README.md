This repository contains tools designed to assist with cross country meet results management and video recording.

Tools Overview
xc_merge_results

The xc_merge_results tool processes Milesplit CSV files for boys and girls teams, combining data and outputting separate CSV and TXT files.

Dependencies

    pandas
    tkinter

Usage

Run the Script:

bash

python xc_merge_results.py

GUI Instructions:

    Click on "Instructions" to open the instructions file.
    Click on "Browse Milesplit CSV File" to select the input CSV file.
    Click on "Convert to Boys and Girls CSV | TXT files" to process the CSV and save the output files.
    Click on "Open CC_Scorer" to open the CC_Scorer.xls file.
    Click on "Open XNoteStopWatch" to open the XNoteStopWatch application.
    Click on "Quit" to exit the program.

File Outputs

    boys_output.csv and girls_output.csv: Processed CSV files for boys and girls teams.
    boys_output.txt and girls_output.txt: Processed TXT files for boys and girls teams.

Functions

    open_instructions(): Opens the instructions HTML file.
    process_milesplit_csv(input_csv): Reads and processes the input CSV file.
    save_to_files(boys_df, girls_df): Saves the processed data to CSV and TXT files.
    browse_csv_file(): Opens a file dialog to select the CSV file.
    convert_csv_to_files(): Processes the CSV file and saves the results.
    open_cc_scores(): Opens the CC_Scorer.xls file.
    open_xnsw(): Opens the XNoteStopWatch application.
    create_gui(): Creates the main GUI for the program.

xc_webcam_stopwatch

The xc_webcam_stopwatch tool captures video from multiple webcams, overlays a stopwatch on the video, and allows recording times to a text file. It also supports screen recording.
Dependencies

    OpenCV (cv2)
    numpy
    pyautogui
    threading
    tkinter

Usage

Run the Script:

bash

python xc_webcam_stopwatch.py

GUI Instructions:

    Click on "Instructions" to open the instructions file.
    Click on "Open XC Merged Results" to open the XC Merged Results application.
    Click on "Set Boys or Girls Time File" to set the output file for recorded times.
    Click on "Start Video Capture" to start capturing video from webcams.
    Click on "Start Timer" to start the stopwatch.
    Click on "Start Screen Recording" to start recording the screen.
    Click on "Stop Screen Recording" to stop the screen recording.
    Click on "Stop Timer" to stop the stopwatch.
    Click on "Stop Video Capture" to stop capturing video from webcams.
    Click on "Quit" to exit the program.

Functions

    update_stopwatch(): Updates the stopwatch display.
    capture_video(device_num, window_name): Captures video from a specified webcam.
    record_screen(): Records the screen.
    start_screen_recording(): Starts the screen recording.
    stop_screen_recording(): Stops the screen recording.
    set_boys_or_girls_time_file(): Sets the output file for recorded times.
    start_video_capture(): Starts capturing video from webcams.
    stop_video_capture(): Stops capturing video from webcams.
    start_timer(): Starts the stopwatch.
    stop_timer(): Stops the stopwatch.
    quit_program(): Quits the program.
    open_xc_merged_results(): Opens the XC Merged Results application.
    open_instructions(): Opens the instructions HTML file.
    create_gui(): Creates the main GUI for the program.

Integration with Other Tools

This project incorporates the use of external tools for enhanced functionality:

    XNote Stopwatch: Used independently for race timing purposes. More information available at XNote Stopwatch.
    CC Scorer: Previously available from Scott's Software, this tool is referenced for cross country scoring functionality.

Affiliation and License

This project is not affiliated with XNote Stopwatch or CC Scorer. It is licensed under the MIT License. Use at your own risk.
Recommendations

For optimal use:

    Use two webcams: one for bib number recording and another for finish line recording.
    Utilize two laptops: one for camera-based finish line recording and another for bib number recording. Save data to a flash drive for scoring.

TODOs

    Incorporate RFID tags for athlete time capture.
