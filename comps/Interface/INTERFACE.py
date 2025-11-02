STICKERS = [
    # Encouragements 🌟
    """<div class="text-xl text-blue-500 font-bold animate-fadeIn">🌟 Good Job!</div>""",
    """<p class="text-lg text-green-500 font-semibold animate-bounce">👏 Well Done!</p>""",
    """<strong class="text-lg text-red-500 font-extrabold animate-slideUp">🔥 Very nice!</strong>""",
    """<h3 class="text-xl text-yellow-500 font-bold animate-fadeIn-cont">💪 Great Job!</h3>""",
    """<em class="text-lg text-pink-500 font-semibold animate-bounce-cont">✨ Great work!</em>""",
    """<blockquote class="text-lg text-indigo-500 font-medium italic animate-pulse-cont">💯 Nice work!</blockquote>""",
    """<h2 class="text-2xl text-orange-500 font-extrabold animate-fadeIn">🎯 Amazing!</h2>""",
    """<div class="text-xl text-cyan-500 font-bold animate-slideUp">🚀 Keep Going!</div>""",
    
    # Appreciation 💖
    """<p class="text-lg text-purple-500 font-medium animate-pulse">💖 You’re awesome!</p>""",
    """<h4 class="text-lg text-rose-500 font-bold animate-bounce-cont">🌈 Fantastic Effort!</h4>""",
    """<span class="text-lg text-lime-600 font-semibold animate-fadeIn">🌿 Nicely Done!</span>""",
    """<div class="text-lg text-amber-600 font-bold animate-fadeIn-cont">🎉 Superb Work!</div>""",
    
    # Celebration 🎊
    """<h2 class="text-2xl text-pink-600 font-extrabold break-words animate-bounce">🎊 Congratulations!</h2>""",
    """<p class="text-lg text-blue-600 font-semibold animate-pulse">🎉 You Did It!</p>""",
    """<strong class="text-lg text-green-600 font-bold animate-fadeIn">🏆 Winner!</strong>""",
    """<div class="text-lg text-yellow-600 font-semibold animate-fadeIn-cont">🥇 Champion!</div>""",
    
    # Motivation 💪
    """<p class="text-lg text-teal-600 font-bold animate-fadeIn">⚡ Keep it up!</p>""",
    """<div class="text-lg text-orange-600 font-semibold animate-pulse-cont">🔥 Don’t stop now!</div>""",
    """<h3 class="text-lg text-emerald-600 font-bold animate-slideUp">🌱 Keep learning!</h3>""",
    """<blockquote class="text-lg text-sky-600 font-medium italic animate-bounce-cont">💫 Keep shining!</blockquote>""",
    """<p class="text-lg text-indigo-600 font-semibold animate-fadeIn-cont">🚀 Aim higher!</p>""",
    
    # Appreciation / Feedback 👍
    """<span class="text-lg text-blue-600 font-semibold animate-fadeIn">👍 Great understanding!</span>""",
    """<p class="text-lg text-violet-500 font-medium animate-pulse">🧠 Smart move!</p>""",
    """<h4 class="text-lg text-pink-600 font-bold animate-bounce">🎨 Creative approach!</h4>""",
    """<div class="text-lg text-green-500 font-bold animate-fadeIn-cont">🧩 Perfect solution!</div>""",
    
    # Friendship / Casual 😄
    """<p class="text-lg text-amber-500 font-medium animate-bounce-cont">😄 Nice talking to you!</p>""",
    """<span class="text-lg text-rose-500 font-semibold animate-pulse">💬 Great chat!</span>""",
    """<div class="text-lg text-lime-600 font-bold animate-fadeIn">👋 Hello there!</div>""",
    """<div class="text-lg text-blue-400 font-bold animate-fadeIn-cont">🌻 Have a great day!</div>""",
    
    # Mini list sticker 📝
    """<ul class="text-lg text-teal-500 font-bold animate-fadeIn">
        <li>🌟 Good Job</li>
        <li>🔥 Keep Going</li>
        <li>🎉 Congrats</li>
    </ul>""",
    
    # Code or creative touch 💻
    """<code class="text-md text-gray-800 font-mono animate-pulse-cont">💻 Code Complete!</code>""",
    """<pre class="text-md text-slate-700 font-mono animate-fadeIn">🧠 Task Done!</pre>""",
    
    # Divider style 🌈
    """<hr class="border-t-4 border-blue-500 animate-slideUp" />""",
    
    # Quote style 💭
    """<blockquote class="text-lg text-gray-700 italic border-l-4 border-purple-400 pl-3 animate-fadeIn-cont">“Keep improving every day!” 💫</blockquote>""",

    # Islamic Greetings 🌙
    """<h2 class="text-2xl text-emerald-600 font-bold animate-fadeIn">🕌 السَّلَامُ عَلَيْكُمْ <br><span class='text-base text-gray-600'>(Assalāmu ʿalaykum)</span></h2>""",
    
    """<h2 class="text-2xl text-blue-600 font-bold animate-fadeIn-cont">🤍 وَعَلَيْكُمُ السَّلَام <br><span class='text-base text-gray-600'>(Wa ʿalaykumu s-salām)</span></h2>""",
    
    # Jummah Mubarak 🌿
    """<div class="text-2xl text-green-600 font-extrabold animate-pulse">🌿 جُمُعَة مُبَارَك 🌿 <br><span class='text-base text-gray-600'>(Jummah Mubarak)</span></div>""",
    
    # Eid Mubarak 🌙🎉
    """<h2 class="text-3xl text-yellow-500 font-extrabold animate-bounce">🌙 عِيد مُبَارَك 🎉 <br><span class='text-base text-gray-600'>(Eid Mubarak)</span></h2>""",

]

ANIMATIONS = {
    "fadeIn": {
        "keyframes": """
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        """,
        "class_string": "animation: fadeIn 0.6s ease-out infinite;"
    },
    "bounce": {
        "keyframes": """
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        """,
        "class_string": "animation: bounce 1s ease-in-out infinite;"
    },
    "pulse": {
        "keyframes": """
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        """,
        "class_string": "animation: pulse 1.5s ease-in-out infinite;"
    },
    "slideUp": {
        "keyframes": """
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        """,
        "class_string": "animation: slideUp 0.6s ease-out infinite;"
    },
    "shake": {
        "keyframes": """
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        """,
        "class_string": "animation: shake 0.6s ease-in-out infinite;"
    },
    "zoomIn": {
        "keyframes": """
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        """,
        "class_string": "animation: zoomIn 0.5s ease-out infinite;"
    },
    "rotateIn": {
        "keyframes": """
            from { transform: rotate(-15deg) scale(0.9); opacity: 0; }
            to { transform: rotate(0) scale(1); opacity: 1; }
        """,
        "class_string": "animation: rotateIn 0.6s ease-out infinite;"
    },
    "wobble": {
        "keyframes": """
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-5deg); }
            75% { transform: rotate(5deg); }
        """,
        "class_string": "animation: wobble 1s ease-in-out infinite;"
    },
    "heartbeat": {
        "keyframes": """
            0%, 100% { transform: scale(1); }
            25% { transform: scale(1.1); }
            50% { transform: scale(0.95); }
            75% { transform: scale(1.05); }
        """,
        "class_string": "animation: heartbeat 1.2s ease-in-out infinite;"
    },
    "glow": {
        "keyframes": """
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.5); }
        """,
        "class_string": "animation: glow 1.5s ease-in-out infinite;"
    },
}
