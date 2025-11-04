# TestGPT: A Generative AI-Based Tool for Testing XR Applications

This repository contains the official code for **TestGPT**, a generative AI-based testing tool for Unity 3D applications. This project was the primary artifact for the Master of Science thesis, **"Evaluating LLM-Generated Test Scripts, Manual Test Development, and Capture-and-Replay Approaches for Testing XR Applications"** completed at the University of Calgary.

**Author:** [Seyed Nami Modarressi](https://github.com/NamiMod)
**Supervisor:** Dr. Frank Maurer

---

## 📖 Project Overview & Thesis Context

Testing Extended Reality (XR) applications is notoriously difficult.  Unlike traditional 2D apps, XR environments involve immersive 3D spaces, spatial awareness, real-time sensor input, and complex user interactions[cite: 86, 87, 88].  These factors make manual testing "labor-intensive and time-consuming", often leading to testing being overlooked.

This research set out to solve this problem by asking two key questions:
1.   How do different testing methods (Manual, Capture-and-Replay, and Generative AI) compare for testing XR applications?
2.   Can generative AI be effective in generating tests based on scene information and natural-language scenarios?

 To answer this, we developed **TestGPT** and conducted an empirical study with 15 participants comparing three distinct testing methodologies.

### The Empirical Study: 3 Methods Compared

 Our study provided participants with a Unity project and had them test six scenarios using each of the following methods:

| Method | Tool Used | Description |
| :--- | :--- | :--- |
| **1. Manual Test Development** |  **Arium Framework** | Participants manually wrote C# test scripts by hand using the Arium framework. |
| **2. Capture-and-Replay** |  **GameDriver** |  Participants recorded their interactions in the scene, and the tool replayed them to validate behavior. |
| **3. Generative AI** |  **TestGPT (This Tool)**  |  Participants provided the Unity scene file and a natural language prompt (e.g., "Test if the cube color changes"), and TestGPT generated the Arium test script automatically. |

---

## 📊 Key Findings & Results

The study yielded clear trade-offs between the three methods.

*  **Manual Coding (Arium):** Offered the highest **control and precision**.  Participants "felt... in command"  and trusted it as the "most reliable" method.  However, it was the slowest, least scalable, and had the highest mental demand.

*  **Capture-and-Replay (GameDriver):** Was overwhelmingly the **fastest and most efficient**.  It was highly intuitive, had the lowest cognitive load, and was great for regression testing.  Its major weakness: it is "sensitive to UI changes" if a button moves, the test breaks.

*  **TestGPT (Our Tool):** Was highly "appreciated for its simplicity and natural-language interface".  It was significantly faster than manual coding and was the **preferred method for complex projects**.  Its main limitation was that it was less effective for highly complex scenarios and was (intentionally) designed *without* conversational memory, which users found frustrating for iterative prompting.

---

## 🤖 What is TestGPT?

TestGPT is a generative AI tool designed to bridge the gap between easy-to-use-tools and powerful, precise test scripts.

It works by taking two inputs:
1.   **A Unity Scene File:** The tool parses the `.yaml` scene file to understand all the GameObjects, their names, components, and attributes.
2.   **A Natural Language Prompt:** The tester writes a simple, high-level test scenario, like *"Test if you can change the color of the cube by clicking on the change color button."*.

 It then generates a complete, executable **C# test script** for the [Arium testing framework](https://github.com/thoughtworks/Arium).

### How It Works: 3-Agent Architecture

TestGPT is not just a simple wrapper for an LLM.  It uses a multi-agent architecture to ensure higher accuracy and reliability[cite: 1068, 1070, 1075].

1.  **Checker Agent:** The user's prompt is first sent to this agent.  Its only job is to verify the request is related to test generation, filtering out unrelated prompts to save costs.
2.   **First Agent (Generator):** This agent receives the prompt, the scene file, and examples of Arium syntax.  It analyzes the scene to find the relevant objects (e.g., "cube" and "change color button") and generates the initial C# test script.
3.  **Controller Agent (Reviewer):** This is the key. The generated code is *not* shown to the user.  Instead, it's passed to this second "automated code reviewer" agent.  This agent checks the code for syntax errors, logical flaws, and ensures it matches the user's scenario, attempting to fix any issues it finds.

Only after passing this review is the final, validated code presented to the user.

### User Workflow


1.  **Upload:** The user uploads their Unity scene file (`.yaml`).
2.  **Write:** The user writes their test scenario in the text box.
3.  **Generate:** TestGPT processes the request through its 3-agent pipeline.
4.  **Copy:** The final C# code appears in the output window.
5.   **Execute:** The user copies this code into their Unity project's test files and runs it using Unity's built-in Test Runner.

---

## 📜 Thesis Information

*  **Title:** Evaluating LLM-Generated Test Scripts, Manual Test Development, and Capture-and-Replay Approaches for Testing XR Applications
*  **Author:** Seyed Nami Modarressi 
*  **Supervisor:** Dr. Frank Maurer 
*  **Institution:** University of Calgary, Faculty of Graduate Studies 
*  **Degree:** Master of Science in Computer Science 
*  **Date:** August 2025 

*(You can link to the official thesis PDF here once it's available in the university's digital archive.)*

## 🚀 Future Work

This research opened several exciting avenues for future work, including:

*  **Adding Conversational Memory:** Implementing chat history to allow users to iteratively refine tests (e.g., "now add an assertion for the color") instead of rewriting the entire prompt[cite: 1624, 1625].
*  **Testing Complex Scenarios:** Evaluating TestGPT on larger, production-level XR applications with asynchronous behaviors and dynamic objects[cite: 1616, 1618].
* **Hybrid Tooling:** Combining Capture-and-Replay with LLM generation.  A user could record an interaction, and the LLM would automatically convert the recorded steps into a readable, editable C# script[cite: 1633, 1636].

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
