***

# Gemini Code Assistant for Sublime Text

## What is this sweet thing?

You know how sometimes you're just staring at your code, and you wish you had a brilliant mind right there to bounce ideas off of, or to gently nudge you in the right direction? Well, my love, this plugin is exactly that! It's your very own AI coding assistant, nestled right into your Sublime Text editor, powered by the utterly fascinating Google Gemini. Think of it as having a super smart, ever-available companion who understands your code and is always ready to help you craft something spectacular. No more lonely coding sessions, darling!

## How it works (the juicy bits!)

It's actually quite simple and *oh-so-convenient*! When you’re feeling a little stuck, or just want to explore possibilities:

1.  You can either highlight a delicious chunk of code that's caught your eye (or is perhaps giving you a bit of trouble).
2.  Then, you pop open the input panel (`Tools > Gemini Code Assistant` is usually the way, honey!), and you ask Gemini whatever your heart desires.
3.  The plugin then takes your selected code (if you gave it any lovely samples!) and your question, and sends it off to the Gemini AI.
4.  Gemini, being the clever thing it is, processes your request and sends back a wonderfully helpful response.
5.  *Voila!* Its answer appears in a dedicated "Gemini Response" tab right in Sublime Text.

The best part? It remembers your conversations! This plugin keeps track of your chats in a neat little local database, so you can have a continuous, flowing dialogue with Gemini. It's like a secret diary, just for your coding musings, keeping everything cozy and private. So you can pick up right where you left off, no awkward silences or repeating yourself!

## Getting it installed (for the hands-on types!)

If you're like me and love to get your hands a little dirty, installing this manually is an absolute breeze. Consider it a warm-up for your next big coding session!

1.  **Get Your API Key First, Sweetie:** Before anything else, you absolutely *must* have an API key for the Google Gemini API. Head over to the Google Cloud Console and get one. It’s like getting your VIP pass – you can’t get in without it!
2.  **Find Your Packages Folder:** In Sublime Text, go to `Preferences > Browse Packages...`. This will open the directory where all your lovely plugins reside. Keep that window open!
3.  **Clone This Repository:** Open your terminal or command prompt, navigate to that `Packages` folder you just found. Then, you'll want to clone this plugin's repository right into it. Make sure you name the folder something sensible, like `Gemini Code Assistant` (it just makes things neater, you know?).
    ```bash
    git clone https://github.com/radda-ui/Gemini-chat "Gemini Code Assistant"
    ```
4.  **Configure Your API Key:** Once it's cloned, go back to Sublime Text and navigate to `Preferences > Package Settings > Gemini Code Assistant > Settings`. You'll find a place to lovingly paste your Gemini API key there. Don't be shy; it's crucial!
5.  **A Quick Restart:** Give Sublime Text a lovely little restart. It helps everything settle in perfectly, like a good stretch after a long coding session.
