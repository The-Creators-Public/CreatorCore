<h1>🤖 CreatorCore</h1>

<p><strong>CreatorCore</strong> is the official Discord bot for the <a href="https://discord.gg/Yds8G7fwJH" target="_blank" rel="noopener noreferrer">Creators Public</a> discord server—a collaborative hub for modders, builders, artists, and innovators. Built with <a href="https://docs.pycord.dev/" target="_blank" rel="noopener noreferrer">Pycord</a> and designed for extensibility, CreatorCore helps manage projects, assist developers, and foster a creative community.</p>

<h2>✨ Features</h2>
<ul class="features">
  <li>🎨 <strong>Creative Tools</strong>: Generate mod ideas, biome names, and more.</li>
  <li>🛠️ <strong>Modding Assistance</strong>: Access mod lists, crafting recipes, and development resources.</li>
  <li>🧠 <strong>Developer Support</strong>: Link to documentation, log feature requests, and display development roadmaps.</li>
  <li>🎉 <strong>Community Engagement</strong>: Participate in events, polls, and showcase contributions.</li>
  <li>🛡️ <strong>Moderation Utilities</strong>: Manage messages, warnings, and user roles.</li>
  <li>🔐 <strong>Admin Controls</strong>: Execute shutdowns, restarts, and deployments securely.</li>
  <li>🤖 <strong>AI Integration</strong>: Utilize OpenAI for code optimization and idea generation.</li>
</ul>

<h2>🚀 Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.8+</li>
  <li><a href="https://docs.pycord.dev/" target="_blank" rel="noopener noreferrer">Pycord</a></li>
  <li><a href="https://pypi.org/project/python-dotenv/" target="_blank" rel="noopener noreferrer">python-dotenv</a></li>
</ul>

<h3>Installation</h3>
<ol>
  <li><strong>Clone the repository:</strong>
    <pre>git clone https://github.com/The-Creators-Public/CreatorCore.git
cd CreatorCore</pre>
  </li>
  <li><strong>Create and activate a virtual environment:</strong>
    <pre>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate</pre>
  </li>
  <li><strong>Install dependencies:</strong>
    <pre>pip install -r requirements.txt</pre>
  </li>
  <li><strong>Configure environment variables:</strong><br>
    Rename <code>.env.example</code> to <code>.env</code>.<br>
    Populate the <code>.env</code> file with your bot token and other necessary configurations.
  </li>
  <li><strong>Run the bot:</strong>
    <pre>python main.py</pre>
  </li>
</ol>

<h2>🧹 Commands Overview</h2>

<table>
  <thead>
    <tr>
      <th>Command</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>/modlist</td><td>Display current mods with links and authors.</td></tr>
    <tr><td>/showcase &lt;mod&gt;</td><td>Show details and status of a selected mod.</td></tr>
    <tr><td>/craft &lt;item&gt;</td><td>Return crafting recipes from the mod database.</td></tr>
    <tr><td>/weather &lt;biome&gt;</td><td>Simulate biome conditions.</td></tr>
    <tr><td>/buildhelp &lt;topic&gt;</td><td>Provide tutorials or code snippets.</td></tr>
    <tr><td>/inspire</td><td>Generate motivational quotes or design ideas.</td></tr>
    <tr><td>/docs</td><td>Link to official documentation and tutorials.</td></tr>
    <tr><td>/issues</td><td>Redirect to GitHub Issues with instructions.</td></tr>
    <tr><td>/request &lt;feature&gt;</td><td>Log a mod feature request or improvement.</td></tr>
    <tr><td>/roadmap</td><td>Show the development roadmap.</td></tr>
    <tr><td>/event</td><td>Display upcoming events or contests.</td></tr>
    <tr><td>/poll &lt;question&gt;</td><td>Create a simple poll.</td></tr>
    <tr><td>/remindme &lt;time&gt; &lt;msg&gt;</td><td>Set a custom user reminder.</td></tr>
    <tr><td>/stats @user</td><td>Pull GitHub commits/PRs using the GitHub API.</td></tr>
    <tr><td>/profile</td><td>Show a user’s mod contributions and roles.</td></tr>
    <tr><td>/suggest &lt;idea&gt;</td><td>Log suggestions to a mod channel or file.</td></tr>
    <tr><td>/clear &lt;num&gt;</td><td>Purge messages.</td></tr>
    <tr><td>/mute, /unmute @user</td><td>Temporarily mute or unmute a user.</td></tr>
    <tr><td>/kick, /ban</td><td>Standard moderation commands.</td></tr>
    <tr><td>/warn</td><td>Add a warning to a user’s internal modlog.</td></tr>
    <tr><td>/modlog</td><td>DM mods recent flags/actions.</td></tr>
    <tr><td>/lockchannel</td><td>Temporarily lock a channel for events.</td></tr>
    <tr><td>/shutdown</td><td>Controlled shutdown (restricted to admins).</td></tr>
    <tr><td>/restart</td><td>Restart the bot.</td></tr>
    <tr><td>/deploy</td><td>Trigger a GitHub Actions or CI/CD deploy.</td></tr>
    <tr><td>/askcore &lt;question&gt;</td><td>Use GPT for coding questions or design help.</td></tr>
    <tr><td>/rewrite &lt;code&gt;</td><td>Clean or optimize pasted code.</td></tr>
    <tr><td>/idea</td><td>Generate mod ideas, biome names, etc.</td></tr>
    <tr><td>/cat, /dog, /mcjoke</td><td>Small, thematic interactions.</td></tr>
    <tr><td>/daily</td><td>Provide a daily creative challenge or trivia.</td></tr>
    <tr><td>/rank</td><td>Show user leveling or creative badges.</td></tr>
  </tbody>
</table>

<p class="note">Note: Replace <code>/</code> with your bot's command prefix if different.</p>

<h2>🛠️ Development</h2>

<h3>Project Structure</h3>
<pre>
CreatorCore/
├── cogs/                 # Modular command and event handlers
├── data/                 # JSON or YAML files for mod data
├── utils/                # Utility functions and helpers
├── main.py               # Bot entry point
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── LICENSE.txt           # Licensing information
</pre>

<h3>Contributing</h3>
<p>We welcome contributions! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.</p>

<h2>📜 License</h2>
<p>This project is licensed under the terms of the MIT License for the source code and Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International for creative content.</p>

<h2>🌐 Links</h2>
<ul>
  <li><a href="https://discord.gg/your-invite-link" target="_blank" rel="noopener noreferrer">Creators Public Discord Server</a></li>
  <li><a href="https://docs.pycord.dev/" target="_blank" rel="noopener noreferrer">Pycord Documentation</a></li>
  <li><a href="https://github.com/The-Creators-Public/CreatorCore" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
</ul>

<p>Crafted with ❤️ by the Creators Public community.</p>

</body>
</html>
