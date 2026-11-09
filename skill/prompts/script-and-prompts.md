# AI Prompts Pack — Copy-Paste Ready

> SKILL.md ke steps ko automate karne wale prompts. {TOPIC}, {LANG}, {DURATION} badal ke use karo.

---

## 1. Research Prompt

```
Mujhe ek YouTube facts video ke liye research chahiye.
TOPIC: {TOPIC}
AUDIENCE: India, 18-34, curious viewers
Mujhe do:
1. 10 verified shocking facts (har ek ke saath source URL)
2. 5 concrete numbers (jinhe video mein use kar sakun)
3. Ek timeline/sequence: origin → problem → solution → twist → present/future
4. Koi real quote ya dialogue (agar kisi real person ne kaha ho)
5. Common myths jo is topic par logon ko hain (jinhe tod sakun)
Constraints: sirf verified facts, koi speculation nahi. Numbers exact hone chahiye.
```

## 2. Script Prompt — SHORTS (English)

```
Write a YouTube Shorts script (330-360 words) in this EXACT structure:

① HOOK (≤25 words): "Would you believe..." + one concrete shock image + stakes
② STINGER: "A [emotion] truth of science and [domain] that will [promise]..."
③ SETUP: context + relatable contrast (For humans X... but for Y...)
④ ESCALATION: 3-4 facts, each bigger than the last, with numbers every 2-3 lines,
   micro-cliffhangers between them ("But then...", "And that's when...")
⑤ TWIST: "But here's the real truth..." + the most surprising reveal
⑥ EMOTIONAL TURN: reframe into awe/moral/pride
⑦ POETIC CLOSE: one quotable line. Last word echoes the first image.

STYLE RULES:
- Sentences 8-14 words. Punch lines 3-5 words.
- Idea/scene change every 12-18 words.
- Direct address: "Think about it", "Now understand this carefully".
- One rhetorical question as a bridge.
- Personify the topic (villain / hero / genius).
- NO intro, NO "welcome back", NO outro ask. Start at the hook. End at the quote.

FACTS TO USE:
{FACT_PACK}
```

## 3. Script Prompt — SHORTS (Hindi)

```
एक YouTube Shorts स्क्रिप्ट लिखो (330-360 शब्द, शुद्ध हिंदी, देवनागरी) इसी स्ट्रक्चर में:

① हुक (≤25 शब्द): "क्या आपको लगता है..." / "क्या आप यकीन करेंगे..." + एक ठोस शॉकिंग इमेज
② स्टिंगर: "विज्ञान का [भावना] सच जो आपको [वादा]..."
③ सेटअप: संदर्भ + तुलना (इंसानों के लिए X... लेकिन Y के लिए...)
④ एस्केलेशन: 3-4 तथ्य, हर एक पिछले से बड़ा, हर 2-3 लाइन में नंबर,
   बीच में माइक्रो-क्लिफहैंगर ("लेकिन तभी...", "और यहीं से शुरू होता है...")
⑧ ट्विस्ट: "लेकिन असली सच तो इसके बाद..." + सबसे चौंकाने वाला खुलासा
⑥ भावनात्मक मोड़: विस्मय/गर्व/ममता में बदलाव
⑦ काव्यात्मक अंत: एक याद रहने वाली लाइन। आखिरी शब्द पहली इमेज की गूंज हो।

नियम:
- वाक्य 8-14 शब्द। पंच लाइन 3-5 शब्द।
- हर 12-18 शब्द पर नई बात/दृश्य।
- सीधा संवाद: "जरा सोचिए", "अब ध्यान से समझिए"
- टॉपिक को किरदार बनाओ (खलनायक/हीरो/जीनियस)
- कोई intro नहीं, कोई "स्वागत है" नहीं। हुक से शुरू, कोट से खत्म।

तथ्य:
{FACT_PACK}
```

## 4. Script Prompt — LONG-FORM (8 min)

```
Write an 8-minute YouTube documentary script (~1,150 words) on {TOPIC}.

STRUCTURE:
① CINEMATIC COLD OPEN (40-50s): "Imagine..." — vivid scene painting of the most
   stunning image in the story. End with: "This is not a scene from a science
   fiction movie. This is [TOPIC REVEAL]."
② PROMISE: "An engineering/medical/natural marvel that most Indians don't know about."
③ ORIGIN STORY (2-2.5 min): dated narrative ("The year was..."), emotional stakes,
   a national/human crisis that started it all.
④ PROBLEM (1 min): "But there was a massive problem..." with vivid failure scenarios.
⑤ SOLUTION + SCIENCE (1.5-2 min): the brilliant idea, specs/numbers,
   "Now, understand this carefully" explainer section.
⑥ TWIST CHAPTER (50s): "But the story doesn't end here" — a smart modern example.
⑦ SCALE + FUTURE (40s): "How much is that?" scale comparison + expansion plans.
⑧ CALLBACK + PRIDE CTA (15-20s): mirror the opening image with a transformation
   ("In [year] we had to X, and today..."), then: "If you are also proud... like,
   share, subscribe."

RULES: rhetorical questions as bridges; one dialogue reenactment; numbers every
20-30s; short punch sentences after long ones; chapter titles as on-screen text.

FACTS:
{FACT_PACK}
```

## 5. Visual Shot-List Prompt

```
Is script ke liye shot list banao. Har clause ke saath:
- Visual type (stock footage / AI still / AI clip / map / diagram / stat card)
- AI image generation prompt (Midjourney style, cinematic, teal-orange grade,
  16:9 or 9:16, "documentary photography, dramatic lighting")
- SFX suggestion (whoosh / impact / riser / ambience)
- Text overlay (keyword ya number)

SCRIPT:
{SCRIPT}
```

## 6. ElevenLabs VO Settings (per section)

```
Hook:       stability 45%, style 65%, speed 1.08  (conspiratorial intensity)
Escalation: stability 50%, style 60%, speed 1.10  (building urgency)
Twist:      stability 55%, style 70%, speed 0.98  (slow down, gravity)
Emotion:    stability 60%, style 55%, speed 0.95  (warm, soft)
Close:      stability 55%, style 60%, speed 1.00  (pride, slight smile)
```

## 7. Thumbnail Prompt (Midjourney)

```
/imagine prompt: cinematic documentary still, {SUBJECT}, dramatic teal-orange
color grade, dark moody atmosphere, volumetric light, shallow depth of field,
space on left side for bold text, hyper-realistic, 16:9 --ar 16:9 --v 6
```

3 variants: (a) subject + glowing number prop, (b) split composition before/after,
(c) extreme close-up of the shocking element + scale reference.

## 8. Title Generator Prompt

```
5 YouTube titles do for {TOPIC}:
- 3 shock/fear style ("The X That Y...", "The Z That Could...")
- 2 question style ("Why Does...", "How Did...")
Rules: concrete noun zaroor ho, spoiler nahi, curiosity gap, ≤60 chars,
emoji 1 max (😨 or 🫪). Hindi mein bhi 2 variants do.
```

## 9. Hook Rewriter (Weak Hook Fix)

```
Is hook ko 3x stronger banao. Rules: concrete image 2 words mein, stakes
immediately, "would you believe" ya "kya aapko lagta hai" opener,
≤25 words, no generic promise.

Current hook: {HOOK}
```

## 10. Fact-Check Prompt (Trust Layer)

```
In claims ko verify karo. Har claim ke liye: TRUE / FALSE / MISLEADING + source URL
+ corrected version. Koi claim bina source ke accept mat karo.

Claims:
{SCRIPT_FACTS}
```
