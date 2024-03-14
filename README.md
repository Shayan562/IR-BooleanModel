# Information Retrieval - Boolean Model

This project implements the basic boolean model for information retrieval on a static set of documents. It supports two types of queries: boolean and proximity.

## Features
- **Indexing**: If an index already exists, the system loads it. Otherwise, it creates a new one.
- **Document Reading**: The system reads a given set of documents.
- **Tokenization**: The text from the documents is tokenized.
- **Text Cleaning**: The system removes stop words, punctuations, alpha-numeric words, and more.
- **Storage**: The cleaned tokens are stored in the index/set which is stored locally.
- **Query Interface**: The system provides an interface for the user to run a query.

## Getting Started
To run the project, you must complie it yourself. The file/folder structure will stay the same; you will require all the files in the repo. You will need python and the libraries nltk, re, string, os, pickle, and PySimpleGUI. Then complie/run the main.py.
To use custom files one must add the files in the code. The filenames will be added in the list called "Files" in "main.py". If the executable has been run before, a file called "index.pickle" will be present by the code; it is to be deleted to update the index for the new files.

