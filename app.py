from flask import Flask, render_template, request, jsonify
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No API key set for OpenAI. Please set the OPENAI_API_KEY environment variable.")
client = OpenAI(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================
# Arium Framework Syntax and Example Tests for Few-Shot Learning
# ==========================
ATRIUM_SYNTAX = r"""
Arium Framework Syntax Reference:
1. Instantiate Arium:
   var _arium = new Arium();
2. Find GameObjects:
   _arium.FindGameObject("Name");
3. Get Components:
   _arium.GetComponent<Component>("Name");
4. Perform Actions:
   _arium.PerformAction(new UnityPointerClick(), "Name");
5. Unity Event System:
   UnityEventSystemInteraction<T>.PerformAction("Name");
"""

EXAMPLE_TESTS = r"""
using System.Collections;
using AriumFramework;
using AriumFramework.Plugins.UnityCore.Extensions;
using AriumFramework.Plugins.UnityCore.Interactions;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Samples.AriumSample.Tests
{
    public class SampleSceneTests
    {
        private Arium _arium;

        [OneTimeSetUp]
        public void SetUp()
        {
            _arium = new Arium();
            SceneManager.LoadScene("SampleScene");
        }

        [UnityTest, Order(1)]
        public IEnumerator OnClickingChangeColorCubeColorShouldBeChanged()
        {
            yield return new WaitForSeconds(2);
            GameObject cube = _arium.FindGameObject("Cube");
            string changeColorButton = "ChangeColor";
            // Validate default color is white
            Assert.AreEqual(Color.white, cube.GetComponent<MeshRenderer>().material.color);
            // Click → Green
            _arium.PerformAction(new UnityPointerClick(), changeColorButton);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Color.green, cube.GetComponent<MeshRenderer>().material.color);
            // Click → Red
            _arium.PerformAction(new UnityPointerClick(), changeColorButton);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Color.red, cube.GetComponent<MeshRenderer>().material.color);
        }

        [UnityTest, Order(2)]
        public IEnumerator OnResetCubeColorShouldBeChangedAndResetButtonShouldNotBeInteractable()
        {
            yield return new WaitForSeconds(2);
            GameObject cube = _arium.FindGameObject("Cube");
            string resetButton = "Reset";
            Assert.AreNotEqual(Color.white, cube.GetComponent<MeshRenderer>().material.color);
            _arium.PerformAction(new UnityPointerClick(), resetButton);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Color.white, cube.GetComponent<MeshRenderer>().material.color);
            yield return new WaitForSeconds(1);
            Assert.False(TextUtils.IsGameObjectInteractable(_arium.FindGameObject(resetButton)));
        }

        [UnityTest, Order(3)]
        public IEnumerator VerifyCubePositionIsZeroByDefault()
        {
            yield return new WaitForSeconds(2);
            GameObject cube = _arium.FindGameObject("Cube");
            Assert.AreEqual(Vector3.zero, cube.GetComponent<Transform>().position);
            yield return null;
        }

        [UnityTest, Order(4)]
        public IEnumerator VerifyCubePositionIsChangedOnClickingOnChangePosition()
        {
            yield return new WaitForSeconds(2);
            GameObject cube = _arium.FindGameObject("Cube");
            string changePosition = "ChangePosition";
            Assert.AreEqual(Vector3.zero, cube.GetComponent<Transform>().position);
            yield return null;
            // Move Up
            _arium.PerformAction(new UnityPointerClick(), changePosition);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Vector3.up, cube.GetComponent<Transform>().position);
            // Move Right
            _arium.PerformAction(new UnityPointerClick(), changePosition);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Vector3.right, cube.GetComponent<Transform>().position);
            // Move Down
            _arium.PerformAction(new UnityPointerClick(), changePosition);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Vector3.down, cube.GetComponent<Transform>().position);
            // Move Left
            _arium.PerformAction(new UnityPointerClick(), changePosition);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Vector3.left, cube.GetComponent<Transform>().position);
            // Reset
            _arium.PerformAction(new UnityPointerClick(), changePosition);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Vector3.zero, cube.GetComponent<Transform>().position);
            yield return null;
        }

        [UnityTest, Order(5)]
        public IEnumerator OnClickingChangeColorThirdTimeCubeColorShouldBeBlack()
        {
            yield return new WaitForSeconds(2);
            GameObject cube = _arium.FindGameObject("Cube");
            string changeColorButton = "ChangeColor";
            Assert.AreEqual(Color.white, cube.GetComponent<MeshRenderer>().material.color);
            // 1st → Green
            _arium.PerformAction(new UnityPointerClick(), changeColorButton);
            yield return new WaitForSeconds(1);
            // 2nd → Red
            _arium.PerformAction(new UnityPointerClick(), changeColorButton);
            yield return new WaitForSeconds(1);
            // 3rd → Black
            _arium.PerformAction(new UnityPointerClick(), changeColorButton);
            yield return new WaitForSeconds(1);
            Assert.AreEqual(Color.black, cube.GetComponent<MeshRenderer>().material.color);
            yield return null;
        }
    }
}
"""

# ==========================
# Helper Functions
# ==========================
def is_test_generation_prompt(prompt: str) -> bool:
    system_message = (
        "You are an assistant that determines whether a given prompt is related to Unity/XR test generation. "
        "Reply with 'Yes' or 'No' only."
    )
    user_message = f"Is the following prompt related to Unity test generation?\n\nPrompt: {prompt}"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
        )
        return response.choices[0].message.content.strip().lower() == "yes"
    except Exception as e:
        logger.error(f"Error in relevance check: {e}")
        return False

def generate_test(prompt: str, file_content: str) -> dict:
    system_message = (
        "You are an expert at generating Unity C# tests using the Arium Framework. "
        "Use ONLY the syntax below and follow the example tests exactly. "
        f"\n\n{ATRIUM_SYNTAX}\n{EXAMPLE_TESTS}\n"
        "Generate a new test class based on the user scenario and scene file. "
        "Output only the C# code enclosed in ```csharp fences."
    )
    user_message = f"Test Scenario:\n{prompt}\n\nScene File:\n{file_content}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        max_tokens=2000
    )
    code = response.choices[0].message.content.strip()
    if not code.startswith("```csharp"):
        code = f"```csharp\n{code}\n```"
    return {"answer": code}

# ==========================
# Flask Routes
# ==========================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        prompt = request.form.get('prompt', '').strip()
        file = request.files.get('file')
        if not file or not file.filename.lower().endswith(('.yaml', '.yml', '.unity')):
            return jsonify({'error': 'Attach a .unity or .yaml file.'}), 400
        content = file.read().decode('utf-8')
        if not prompt:
            return jsonify({'error': 'Prompt is required.'}), 400
        if len(prompt) > 128000:
            return jsonify({'error': 'Prompt too long.'}), 400
        if not is_test_generation_prompt(prompt):
            return jsonify({'error': 'Prompt not related to test generation.'}), 400
        result = generate_test(prompt, content)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in /submit: {e}")
        return jsonify({'error': 'Internal error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
