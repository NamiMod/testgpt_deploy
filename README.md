# TestGPT: A Generative AI-Based Tool for Testing XR Applications

This repository contains the official code for **TestGPT**, a generative AI-based testing tool for Unity 3D applications. [cite_start]This project was the primary artifact for the Master of Science thesis, **"Evaluating LLM-Generated Test Scripts, Manual Test Development, and Capture-and-Replay Approaches for Testing XR Applications"**[cite: 2, 3], completed at the University of Calgary.

[cite_start]**Author:** [Seyed Nami Modarressi](https://github.com/NamiMod) [cite: 5]
[cite_start]**Supervisor:** Dr. Frank Maurer [cite: 29]

---

## 📖 Project Overview & Thesis Context

Testing Extended Reality (XR) applications is notoriously difficult. [cite_start]Unlike traditional 2D apps, XR environments involve immersive 3D spaces, spatial awareness, real-time sensor input, and complex user interactions[cite: 86, 87, 88]. [cite_start]These factors make manual testing "labor-intensive and time-consuming" [cite: 15][cite_start], often leading to testing being overlooked[cite: 16].

This research set out to solve this problem by asking two key questions:
1.  [cite_start]How do different testing methods (Manual, Capture-and-Replay, and Generative AI) compare for testing XR applications? [cite: 128]
2.  [cite_start]Can generative AI be effective in generating tests based on scene information and natural-language scenarios? [cite: 129]

[cite_start]To answer this, we developed **TestGPT** and conducted an empirical study with 15 participants [cite: 20] comparing three distinct testing methodologies.

### The Empirical Study: 3 Methods Compared

[cite_start]Our study provided participants with a Unity project and had them test six scenarios [cite: 663] using each of the following methods:

| Method | Tool Used | Description |
| :--- | :--- | :--- |
| **1. Manual Test Development** | [cite_start]**Arium Framework** [cite: 779] | Participants manually wrote C# test scripts by hand using the Arium framework. |
| **2. Capture-and-Replay** | [cite_start]**GameDriver** [cite: 780] | [cite_start]Participants recorded their interactions in the scene, and the tool replayed them to validate behavior[cite: 1140, 1141]. |
| **3. Generative AI** | [cite_start]**TestGPT (This Tool)** [cite: 913] | [cite_start]Participants provided the Unity scene file and a natural language prompt (e.g., "Test if the cube color changes")[cite: 19, 970], and TestGPT generated the Arium test script automatically. |

---

## 📊 Key Findings & Results

The study yielded clear trade-offs between the three methods.

* [cite_start]**Manual Coding (Arium):** Offered the highest **control and precision**[cite: 23]. [cite_start]Participants "felt... in command" [cite: 1478] [cite_start]and trusted it as the "most reliable" method[cite: 1485]. [cite_start]However, it was the slowest, least scalable, and had the highest mental demand[cite: 23, 1482, 1386].

* [cite_start]**Capture-and-Replay (GameDriver):** Was overwhelmingly the **fastest and most efficient**[cite: 1286, 1299]. [cite_start]It was highly intuitive, had the lowest cognitive load, and was great for regression testing[cite: 25, 1385, 1520]. [cite_start]Its major weakness: it is "sensitive to UI changes" [cite: 25, 1508]—if a button moves, the test breaks.

* [cite_start]**TestGPT (Our Tool):** Was highly "appreciated for its simplicity and natural-language interface"[cite: 1487]. [cite_start]It was significantly faster than manual coding [cite: 1305] [cite_start]and was the **preferred method for complex projects**[cite: 1576]. [cite_start]Its main limitation was that it was less effective for highly complex scenarios [cite: 24] [cite_start]and was (intentionally) designed *without* conversational memory, which users found frustrating for iterative prompting[cite: 1493, 1557].

[cite_start] [cite: 1317] [cite_start] [cite: 1358]

---

## 🤖 What is TestGPT?

TestGPT is a generative AI tool designed to bridge the gap between easy-to-use-tools and powerful, precise test scripts.

It works by taking two inputs:
1.  [cite_start]**A Unity Scene File:** The tool parses the `.yaml` scene file to understand all the GameObjects, their names, components, and attributes[cite: 789, 917].
2.  [cite_start]**A Natural Language Prompt:** The tester writes a simple, high-level test scenario, like *"Test if you can change the color of the cube by clicking on the change color button."*[cite: 970].

[cite_start]It then generates a complete, executable **C# test script** for the [Arium testing framework](https://github.com/thoughtworks/Arium)[cite: 916].

### How It Works: 3-Agent Architecture

TestGPT is not just a simple wrapper for an LLM. [cite_start]It uses a multi-agent architecture to ensure higher accuracy and reliability[cite: 1068, 1070, 1075].

1.  **Checker Agent:** The user's prompt is first sent to this agent. [cite_start]Its only job is to verify the request is related to test generation, filtering out unrelated prompts to save costs[cite: 1075, 1076].
2.  [cite_start]**First Agent (Generator):** This agent receives the prompt, the scene file, and examples of Arium syntax[cite: 1078]. [cite_start]It analyzes the scene to find the relevant objects (e.g., "cube" and "change color button") and generates the initial C# test script[cite: 1071].
3.  **Controller Agent (Reviewer):** This is the key. The generated code is *not* shown to the user. [cite_start]Instead, it's passed to this second "automated code reviewer" agent[cite: 1070]. [cite_start]This agent checks the code for syntax errors, logical flaws, and ensures it matches the user's scenario, attempting to fix any issues it finds[cite: 1074, 1086].

Only after passing this review is the final, validated code presented to the user.

### User Workflow

[cite_start] [cite: 999]

1.  **Upload:** The user uploads their Unity scene file (`.yaml`).
2.  **Write:** The user writes their test scenario in the text box.
3.  **Generate:** TestGPT processes the request through its 3-agent pipeline.
4.  **Copy:** The final C# code appears in the output window.
5.  [cite_start]**Execute:** The user copies this code into their Unity project's test files and runs it using Unity's built-in Test Runner[cite: 968].

---

## 📜 Thesis Information

* [cite_start]**Title:** Evaluating LLM-Generated Test Scripts, Manual Test Development, and Capture-and-Replay Approaches for Testing XR Applications [cite: 2, 3]
* [cite_start]**Author:** Seyed Nami Modarressi [cite: 5]
* [cite_start]**Supervisor:** Dr. Frank Maurer [cite: 29]
* [cite_start]**Institution:** University of Calgary, Faculty of Graduate Studies [cite: 1, 7]
* [cite_start]**Degree:** Master of Science in Computer Science [cite: 8, 9]
* [cite_start]**Date:** August 2025 [cite: 11]

*(You can link to the official thesis PDF here once it's available in the university's digital archive.)*

## 🚀 Future Work

This research opened several exciting avenues for future work, including:

* [cite_start]**Adding Conversational Memory:** Implementing chat history to allow users to iteratively refine tests (e.g., "now add an assertion for the color") instead of rewriting the entire prompt[cite: 1624, 1625].
* [cite_start]**Testing Complex Scenarios:** Evaluating TestGPT on larger, production-level XR applications with asynchronous behaviors and dynamic objects[cite: 1616, 1618].
* **Hybrid Tooling:** Combining Capture-and-Replay with LLM generation. [cite_start]A user could record an interaction, and the LLM would automatically convert the recorded steps into a readable, editable C# script[cite: 1633, 1636].

## Citation

If you use this work in your research, please cite the original thesis:

```bibtex
@mastersthesis{Modarressi2025,
  author  = {Seyed Nami Modarressi},
  title   = {Evaluating LLM-Generated Test Scripts, Manual Test Development, and Capture-and-Replay Approaches for Testing XR Applications},
  school  = {University of Calgary},
  year    = {2025},
  month   = {August},
  address = {Calgary, AB}
}
