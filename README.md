
- This Python project is a Text-to-Speech (TTS) converter with a graphical user interface (GUI) built using the Tkinter library. 
  The application allows users to input the URL of web articles or upload PDF-format books. The reading process employs
  multi-threading for improved efficiency.

- Here's a breakdown of the key features:

  1) Input Source: Users can provide a URL pointing to web articles or upload PDF-format books.

  2) Multi-threading: The application utilizes multi-threading to enhance performance. As each line is downloaded, the reading of that line begins, and simultaneously, the next line is fetched for download.

  3) Text-to-Speech Conversion: The core functionality involves converting text from the provided sources into speech. This is done line by line, and the multi-threading approach ensures a smooth and parallel processing of downloading and reading.

  4) GUI with Tkinter: The graphical user interface is implemented using Tkinter, a popular Python library for creating GUI applications. This allows users to interact with the application easily.

Overall, this project provides a convenient way for users to have web articles or PDF books read aloud to them, with the added benefit of parallel processing through multi-threading for improved speed and responsiveness.
