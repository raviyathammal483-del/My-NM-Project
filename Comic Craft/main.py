from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>ComicCraftAI</title>

    <style>
        body {
            font-family: Arial;
            background: #eaf6ff;
            text-align: center;
            margin: 0;
        }

        header {
            background: #7ec8e3;
            padding: 25px;
            color: white;
        }

        .container {
            width: 80%;
            margin: 30px auto;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 4px 15px #aaa;
        }

        textarea {
            width: 90%;
            height: 120px;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #aaa;
            font-size: 16px;
        }

        button {
            margin-top: 20px;
            padding: 12px 30px;
            background: #4aa3df;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 17px;
            cursor: pointer;
        }

        .comic {
            margin-top: 30px;
            display: flex;
            justify-content: center;
            gap: 15px;
        }

        .panel {
            width: 180px;
            height: 180px;
            border: 3px solid #333;
            background: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
        }
    </style>
</head>

<body>

<header>
    <h1>🎨 ComicCraftAI</h1>
    <p>Create Your Own Comic Story</p>
</header>

<div class="container">

    <h2>✨ Comic Generator</h2>

    <p>Enter your story below:</p>

    <textarea id="story"
        placeholder="Example: A girl goes to school and finds a magical book...">
    </textarea>

    <br>

    <button onclick="generateComic()">
        Generate Comic
    </button>

    <div id="result"></div>

</div>

<script>

function generateComic() {

    let story = document.getElementById("story").value;

    if (story.trim() === "") {
        alert("Please enter a story!");
        return;
    }

    document.getElementById("result").innerHTML = `
        <h2>📖 Your Comic</h2>

        <div class="comic">

            <div class="panel">
                <b>Panel 1</b><br>
                ${story}
            </div>

            <div class="panel">
                <b>Panel 2</b><br>
                The story continues...
            </div>

            <div class="panel">
                <b>Panel 3</b><br>
                The adventure begins!
            </div>

        </div>
    `;
}

</script>

</body>
</html>
"""

