import logging
import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ============================================================
# ⚙️ APNI SETTINGS YAHAN BHARO
# ============================================================
BOT_TOKEN = "7898119257:AAGJUe7U-H0NYnvvftDZ1-nhbmoi8Rgo3Gs"

# 4 Channel ke usernames (@ ke bina) ya IDs
CHANNELS = [
    {"id": -6714117576, "name": "Channel 1", "link": "https://t.me/apktitann"},
    {"id": -6714117576, "name": "Channel 2", "link": "https://t.me/apktitann"},
    {"id": -6714117576, "name": "Channel 3", "link": "https://t.me/apktitann"},
    {"id": -6714117576, "name": "Channel 4", "link": "https://t.me/apktitann"},
]

# Welcome image URL (koi bhi direct image link)
WELCOME_IMAGE = "https://t.me/c/3173362746/2"

# How To Use video links
HOW_TO_USE_LINK = "https://youtube.com/shorts/00twFmNq0NU?si=vgg_TsKDnpd9RKYU"
BACKUP_CHANNEL_LINK = "https://t.me/apktitan"

# Premium App section ke liye welcome image
PREMIUM_APP_IMAGE = "https://t.me/c/3173362746/2"

# ============================================================
# 📦 APP FILES - Yahan apni apps ki info daalo
# Telegram par apni APK file upload karke uska file_id daalo
# ============================================================
APP_DATABASE = {
    "hill climb": {
        "file_id": "BQACAgIAAxkBAAIB...HILL_CLIMB_FILE_ID",
        "name": "Hill Climb Racing",
        "caption": "✅ *Hill Climb Racing* - Premium Mod\n\n📦 Size: ~50MB\n⭐ Features: Unlimited Money, All Cars Unlocked"
    },
    "hill climb racing": {
        "file_id": "BQACAgIAAxkBAAIB...HILL_CLIMB_FILE_ID",
        "name": "Hill Climb Racing",
        "caption": "✅ *Hill Climb Racing* - Premium Mod\n\n📦 Size: ~50MB\n⭐ Features: Unlimited Money, All Cars Unlocked"
    },
    "pubg": {
        "file_id": "BQACAgIAAxkBAAIB...PUBG_FILE_ID",
        "name": "PUBG Mobile",
        "caption": "✅ *PUBG Mobile* - Mod Version\n\n📦 Features: Aimbot, WallHack"
    },
    "capcut": {
        "file_id": "BQACAgIAAxkBAAIB...CAPCUT_FILE_ID",
        "name": "CapCut Pro",
        "caption": "✅ *CapCut Pro* - Premium Unlocked\n\n📦 All Premium Features Free!"
    },
    "canva": {
        "file_id": "BQACAgIAAxkBAAIB...CANVA_FILE_ID",
        "name": "Canva Pro",
        "caption": "✅ *Canva Pro* - Premium Unlocked\n\n📦 All Templates & Features Free!"
    },
    # Aur apps add karte raho isi format mein
}

# ============================================================
# 📝 CONTENT DATA
# ============================================================

TELEGRAM_CONTENT = {
    "msg_sent_problem": """📨 *Message Sent Problem Solution*

Hello Friends! Kaise Ho? 😊

Agar aapko Telegram mein message send karne mein problem aa rahi hai, to yeh tips follow karo:

1️⃣ *Account Restricted?*
   - Settings > Privacy & Security check karo
   - Agar restricted hai to 24 hours wait karo

2️⃣ *Slow Mode Problem?*
   - Group admin se slow mode band karne ko kaho
   - Ya dusre group try karo

3️⃣ *Spam Block?*
   - @SpamBot se contact karo
   - "I'm not a spammer" likho

4️⃣ *Network Issue?*
   - VPN use karo
   - Data/WiFi switch karo

✅ *Yeh karo aur problem solve ho jayegi!*"""
}

INSTAGRAM_CONTENT = {
    "insta1": """📸 *Instagram Growth Tips - Part 1*

Hello Friends! Kaise Ho? 😊

🚀 *Instagram Par Fast Grow Karo:*

1️⃣ *Profile Optimize karo*
   - Clear profile pic lagao
   - Bio mein keywords daalo
   - Link in bio use karo

2️⃣ *Content Strategy*
   - Daily 1-2 posts karo
   - Reels banao (fastest growth)
   - Stories daily post karo

3️⃣ *Best Posting Time*
   - Morning: 7-9 AM
   - Evening: 6-9 PM

4️⃣ *Hashtag Strategy*
   - 5-10 targeted hashtags use karo
   - Mix of small & big hashtags

✅ *Consistently follow karo, results milenge!*""",

    "insta2": """💰 *Instagram Se Paise Kamao - Part 2*

Hello Friends! Kaise Ho? 😊

💎 *Instagram Monetization Methods:*

1️⃣ *Brand Deals*
   - 10K+ followers hone par brands contact karo
   - Niche specific content banao

2️⃣ *Affiliate Marketing*
   - Amazon/Flipkart affiliate join karo
   - Products promote karo

3️⃣ *Sell Your Services*
   - Photo editing
   - Content writing
   - Social media management

4️⃣ *Instagram Shop*
   - Apna product sell karo
   - Digital products bhi sell ho sakte hain

✅ *Mehnat karo, success zaroor milegi!*"""
}

YOUTUBE_CATEGORIES = {
    "gaming": {
        "name": "🎮 Gaming",
        "hashtag": """🎮 *Gaming YouTube Hashtags*

#gaming #gamer #gameplay #videogames #gamingcommunity #pcgaming #mobilegaming #freefire #pubg #bgmi #minecraft #roblox #among us #gta5 #valorant #fortnite #gaming2024 #gamingvideos #youtubegaming #livestreaming #esports #gamingsetup #gaminglife #pro gamer #gaming shorts #viral gaming #trending gaming #hindi gaming #indian gamer #gaming channel""",

        "keyword": """🎮 *Gaming YouTube Keywords*

✅ *High Search Keywords:*
• free fire gameplay hindi
• pubg mobile tips and tricks
• minecraft survival series hindi
• how to get free UC in bgmi
• best gaming setup under budget
• gaming room tour india
• top 10 mobile games 2024
• free fire best settings
• how to improve aim in pubg
• gaming headphones review hindi

🔥 *Trending Keywords:*
• viral gaming moments
• epic gaming highlights
• satisfying gaming clips
• funny gaming moments hindi"""
    },

    "cooking": {
        "name": "🍳 Cooking",
        "hashtag": """🍳 *Cooking YouTube Hashtags*

#cooking #recipe #food #homemade #indianfood #desikhana #cookingathome #easyrecipe #quickrecipe #streetfood #biryani #dal #sabzi #roti #snacks #breakfast #lunch #dinner #sweets #dessert #healthyfood #vegetarian #nonveg #cookingvideo #kitchentips #foodlover #yummy #delicious #homechef #cookingchannel""",

        "keyword": """🍳 *Cooking YouTube Keywords*

✅ *High Search Keywords:*
• easy breakfast recipe hindi
• quick dinner ideas indian
• biryani recipe restaurant style
• how to make soft roti
• street food recipe at home
• healthy lunch box ideas
• dal tadka recipe dhaba style
• chicken curry simple recipe
• sweet recipes for festivals
• cooking tips for beginners

🔥 *Trending Keywords:*
• 5 minute recipe
• one pot meal
• budget meal ideas
• kids tiffin recipes"""
    },

    "tech": {
        "name": "💻 Tech & Review",
        "hashtag": """💻 *Tech YouTube Hashtags*

#technology #tech #techreview #smartphone #android #iphone #laptop #gadgets #unboxing #review #budget phone #flagship #comparison #techtips #technews #ai #artificialintelligence #chatgpt #techinindia #hinditech #techcreator #gadgetreview #earbuds #smartwatch #gaming laptop #best phone 2024 #value for money #techbhai #techburner #technical guruji""",

        "keyword": """💻 *Tech YouTube Keywords*

✅ *High Search Keywords:*
• best phone under 15000 2024
• smartphone comparison hindi
• budget earbuds review india
• laptop buying guide hindi
• how to speed up android phone
• best apps for students 2024
• iphone vs android which is better
• gaming phone under 20000
• smartwatch review hindi
• free fire best device settings

🔥 *Trending Keywords:*
• unboxing video hindi
• honest review hindi
• best buy in india
• value for money gadgets"""
    },

    "education": {
        "name": "📚 Education",
        "hashtag": """📚 *Education YouTube Hashtags*

#education #learning #study #students #school #college #exam #upsc #ssc #competitive exam #gk #currentaffairs #motivation #selfimprovement #skills #onlinelearning #hindi education #study tips #exam tips #success #career guidance #job #interview tips #english speaking #personality development #knowledge #facts #science #history #geography""",

        "keyword": """📚 *Education YouTube Keywords*

✅ *High Search Keywords:*
• upsc preparation strategy hindi
• ssc cgl study plan
• how to study effectively hindi
• english speaking tips for beginners
• general knowledge questions 2024
• current affairs today hindi
• motivational video hindi
• career guidance after 12th
• how to crack government exam
• interview tips in hindi

🔥 *Trending Keywords:*
• daily current affairs
• amazing facts hindi
• science facts in hindi
• history of india hindi"""
    },

    "entertainment": {
        "name": "🎭 Entertainment",
        "hashtag": """🎭 *Entertainment YouTube Hashtags*

#entertainment #funny #comedy #viral #trending #memes #roast #shorts #youtubeshorts #funnyvideo #comedy video #desi comedy #hindi comedy #prank #challenge #reaction #vlog #dailyvlog #lifevlog #travel #adventure #fun #entertainment channel #viral video #trending video #funny moments #comedy shorts #india entertainment #youtube viral""",

        "keyword": """🎭 *Entertainment YouTube Keywords*

✅ *High Search Keywords:*
• funny videos hindi 2024
• comedy shorts viral
• best prank videos india
• reaction video trending songs
• daily vlog hindi
• travel vlog india budget
• challenge videos hindi
• roast video funny
• desi comedy skits
• family entertainment hindi

🔥 *Trending Keywords:*
• viral shorts 2024
• trending challenge
• funny moments compilation
• comedy reaction video"""
    },

    "fitness": {
        "name": "💪 Fitness",
        "hashtag": """💪 *Fitness YouTube Hashtags*

#fitness #gym #workout #exercise #health #bodybuilding #weightloss #yoga #motivation #fitnessmotivation #gymlife #fitfam #healthylifestyle #diet #nutrition #homeWorkout #abs #sixpack #muscle #strength #cardio #running #cycling #sports #fitnessindia #hindi fitness #gym tips #workout routine #healthy eating #transformation""",

        "keyword": """💪 *Fitness YouTube Keywords*

✅ *High Search Keywords:*
• gym workout for beginners hindi
• home workout no equipment
• how to lose weight fast hindi
• diet plan for weight loss indian
• bodybuilding tips in hindi
• six pack abs workout hindi
• yoga for beginners hindi
• best pre workout foods
• how to build muscle fast
• fitness transformation hindi

🔥 *Trending Keywords:*
• 30 day fitness challenge
• morning workout routine
• gym motivation hindi
• diet plan indian food"""
    }
}

FACEBOOK_CATEGORIES = {
    "reels": {
        "name": "🎬 Facebook Reels",
        "hashtag": """🎬 *Facebook Reels Hashtags*

#facebookreels #reels #viral #trending #fbreels #viralreels #reelsvideo #reelsfb #trending reels #viral video #facebook viral #shortsvideo #reelsindia #hindireels #desi reels #facebook shorts #viralcontent #trending now #explore #foryou #foryoupage #reelitfeelit #reelkarofeelkaro #viralpost #trendingvideo #facebookvideo #socialMedia #content creator""",

        "keyword": """🎬 *Facebook Reels Keywords*

✅ *High Search Keywords:*
• viral facebook reels ideas
• how to go viral on facebook
• facebook reels tips hindi
• best time to post on facebook
• facebook algorithm 2024
• how to get more views on facebook
• facebook reels monetization
• grow facebook page fast
• facebook viral content ideas
• facebook marketing hindi

🔥 *Trending Content Ideas:*
• motivational quotes reels
• before after transformation
• tutorial reels
• funny relatable content"""
    },

    "page_growth": {
        "name": "📈 Page Growth",
        "hashtag": """📈 *Facebook Page Growth Hashtags*

#facebookpage #pagelike #followme #viral #trending #socialmedia #digitalmarketing #facebook #socialmediatips #contentcreator #onlinemarketing #facebookmarketing #growyourbusiness #smallbusiness #entrepreneur #startup #businesstips #marketing #branding #onlinebusiness #makemoneyonline #passiveincome #digitalcreator #influencer #creator #facebookgrowth #organicgrowth #socialmediagrowth""",

        "keyword": """📈 *Facebook Page Growth Keywords*

✅ *High Search Keywords:*
• how to grow facebook page 2024
• get 1000 likes on facebook page
• facebook page monetization requirements
• how to monetize facebook page india
• facebook stars earning hindi
• facebook bonus program india
• best niche for facebook page
• viral post ideas facebook
• facebook engagement tricks
• facebook paid promotion tips hindi

🔥 *Trending Keywords:*
• facebook page grow fast
• organic reach facebook
• facebook content strategy
• page like increase kaise kare"""
    },

    "earning": {
        "name": "💰 Facebook Earning",
        "hashtag": """💰 *Facebook Earning Hashtags*

#facebookearning #earnmoney #onlineearning #makemoneyonline #facebookmonetization #passiveincome #sidehustle #earnfromhome #workfromhome #onlineincome #digitalincome #facebookstars #instreams ads #bonus program #reels play bonus #facebookcreator #contentcreation #creatorportal #socialmediaearning #earnwithfacebook #faceBookMoney #onlinepaisekamao #gharbaithekamao""",

        "keyword": """💰 *Facebook Earning Keywords*

✅ *High Search Keywords:*
• facebook se paise kaise kamaye
• facebook monetization kaise karein
• facebook stars kaise milte hain
• in-stream ads requirements facebook
• facebook reels bonus program india
• facebook creator studio tutorial
• how much facebook pays per view
• facebook earning proof hindi
• facebook page monetization enable
• facebook stars to rupees

🔥 *Trending Keywords:*
• facebook earning 2024
• social media income hindi
• creator economy india
• online earning proof"""
    }
}

GEMINI_CHATGPT_PROMPTS = {
    "styles": """🎨 *Styles Prompt Collection*

🤖 *ChatGPT / Gemini ke liye:*

━━━━━━━━━━━━━━━━━
📝 *Professional Style:*
"Write in a professional, formal tone suitable for business communication. Use clear, concise language and maintain a respectful, authoritative voice throughout."

━━━━━━━━━━━━━━━━━
✍️ *Creative Writer Style:*
"You are a creative writer with 20 years of experience. Write engaging, vivid content with rich descriptions, compelling narratives, and unique metaphors. Make the reader feel emotions."

━━━━━━━━━━━━━━━━━
🎓 *Teacher/Explainer Style:*
"Explain like I'm a 10-year-old. Use simple words, real-life examples, and step-by-step explanations. Include analogies that make complex topics easy to understand."

━━━━━━━━━━━━━━━━━
😄 *Funny/Humorous Style:*
"Write in a witty, humorous tone. Include clever wordplay, funny observations, and light sarcasm. Keep it entertaining while still being informative."

━━━━━━━━━━━━━━━━━
💪 *Motivational Style:*
"Write in an inspiring, motivational tone. Use powerful words, success stories, and call-to-action phrases. Make the reader feel empowered and excited to take action." """,

    "modern": """🚀 *Modern Prompts Collection*

🤖 *Advanced ChatGPT / Gemini Prompts:*

━━━━━━━━━━━━━━━━━
🔥 *Viral Content Creator:*
"Act as a viral content strategist. Create [topic] content that is highly shareable, emotionally engaging, and optimized for social media. Include hooks, storytelling elements, and a strong CTA."

━━━━━━━━━━━━━━━━━
🤖 *AI Persona Prompt:*
"You are an expert AI assistant with deep knowledge in [field]. Respond with confidence, provide data-backed information, cite examples, and offer practical actionable advice."

━━━━━━━━━━━━━━━━━
📊 *Data Analyst Style:*
"Analyze [topic/data] and provide: 1) Key insights 2) Patterns and trends 3) Actionable recommendations 4) Risk factors 5) Future predictions. Use bullet points and be specific."

━━━━━━━━━━━━━━━━━
🎯 *Marketing Expert:*
"As a digital marketing expert, create a complete marketing strategy for [product/service]. Include: target audience, USP, content plan, social media strategy, and KPIs."

━━━━━━━━━━━━━━━━━
💡 *Problem Solver:*
"I have this problem: [describe problem]. Please provide: 1) Root cause analysis 2) Multiple solutions 3) Best solution with reasons 4) Step-by-step implementation plan" """,

    "seo": """🔍 *SEO & Content Prompts*

🤖 *ChatGPT / Gemini SEO Prompts:*

━━━━━━━━━━━━━━━━━
📈 *SEO Blog Writer:*
"Write an SEO-optimized blog post about [topic]. Include: compelling title with keyword, meta description (150 chars), H2/H3 headings, keyword density 1-2%, internal linking suggestions, and a strong conclusion with CTA."

━━━━━━━━━━━━━━━━━
🔑 *Keyword Research Helper:*
"Generate 20 SEO keywords for [niche/topic]. Categorize them as: high volume (informational), buying intent, long-tail keywords, and LSI keywords. Include search intent for each."

━━━━━━━━━━━━━━━━━
📱 *Social Media Caption:*
"Write 5 different Instagram/Facebook captions for [topic/product]. Make them engaging with emojis, include relevant hashtags, and add a clear CTA. Vary the tone: professional, casual, funny, inspiring, and urgent."

━━━━━━━━━━━━━━━━━
🎥 *YouTube Script:*
"Write a YouTube video script for [topic]. Include: attention-grabbing hook (0-15 sec), introduction, 3 main points with examples, transitions, and an engaging outro with subscribe CTA."

━━━━━━━━━━━━━━━━━
📧 *Email Marketing:*
"Write an email marketing campaign for [product/service]. Include: subject line (max 50 chars), preheader, personalized greeting, value proposition, social proof, offer, and clear CTA button text." """,

    "business": """💼 *Business & Freelance Prompts*

🤖 *ChatGPT / Gemini Business Prompts:*

━━━━━━━━━━━━━━━━━
🏢 *Business Plan Creator:*
"Create a detailed business plan for [business idea]. Include: executive summary, market analysis, target audience, revenue model, competitive advantage, marketing strategy, financial projections, and risks."

━━━━━━━━━━━━━━━━━
💰 *Pricing Strategy:*
"Help me price my [product/service]. Analyze: competitor pricing, value perception, target audience budget, cost + margin, and psychological pricing. Recommend optimal pricing with reasoning."

━━━━━━━━━━━━━━━━━
📝 *Proposal Writer:*
"Write a professional freelance proposal for [project/client]. Include: understanding of requirements, proposed solution, timeline, deliverables, pricing, your expertise, and why you're the best choice."

━━━━━━━━━━━━━━━━━
🤝 *Client Communication:*
"Draft a professional message to [client situation - e.g., follow up, delay in delivery, price negotiation]. Tone: confident but respectful. Address their concerns and maintain the relationship."

━━━━━━━━━━━━━━━━━
📊 *Market Research:*
"Conduct market research analysis for [product/niche]. Cover: market size, target demographics, pain points, existing solutions, gaps in market, entry barriers, and opportunity assessment." """
}

# ============================================================
# 🤖 BOT LOGIC
# ============================================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

WAITING_APP_NAME = 1

async def check_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> list:
    """Check which channels user has NOT joined"""
    not_joined = []
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel["id"], user_id)
            if member.status in ['left', 'kicked', 'restricted']:
                not_joined.append(channel)
        except Exception:
            not_joined.append(channel)
    return not_joined

def get_join_keyboard():
    """Channel join buttons banao"""
    buttons = []
    for i, ch in enumerate(CHANNELS):
        buttons.append([InlineKeyboardButton(f"📢 {ch['name']}", url=ch["link"])])
    buttons.append([InlineKeyboardButton("✅ Joined", callback_data="check_joined")])
    return InlineKeyboardMarkup(buttons)

def get_main_menu():
    """6 button wala main menu"""
    keyboard = [
        [InlineKeyboardButton("📱 TELEGRAM", callback_data="menu_telegram"),
         InlineKeyboardButton("📸 INSTAGRAM", callback_data="menu_instagram")],
        [InlineKeyboardButton("▶️ YOUTUBE", callback_data="menu_youtube"),
         InlineKeyboardButton("👥 FACEBOOK", callback_data="menu_facebook")],
        [InlineKeyboardButton("🤖 Gemini+ChatGpt Prompt", callback_data="menu_gemini")],
        [InlineKeyboardButton("💎 PREMIUM APPLICATION", callback_data="menu_premium")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_b
