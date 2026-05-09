import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# =============================================
# BOT TOKEN - BotFather dan olingan tokenni
# shu yerga qo'ying yoki .env faylidan o'qing
# =============================================
BOT_TOKEN = "7606381723:AAGQAv6Z4_2qm99MBTrwtEU2GZBPcygushU"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# =============================================
# TOPISHMOQLAR MA'LUMOT BAZASI
# =============================================
TOPISHMOQLAR = [
    {
        "savol": "Qishda tug'ilgan, bahorda o'ladi. Nima bu?",
        "javob": "qor",
        "maslahat": "Sovuq ob-havo bilan bog'liq"
    },
    {
        "savol": "Ko'zim bor, lekin ko'ra olmayman. Nima bu?",
        "javob": "igna",
        "maslahat": "Tikuvchilik asbob-uskunasi"
    },
    {
        "savol": "Tili bor, lekin gapira olmaydi. Nima bu?",
        "javob": "etik",
        "maslahat": "Oyoqqa kiyiladi"
    },
    {
        "savol": "Har doim yuguradi, lekin oyog'i yo'q. Nima bu?",
        "javob": "suv",
        "maslahat": "Daryoda ko'p bo'ladi"
    },
    {
        "savol": "Eshigi bor, lekin kirish mumkin emas. Nima bu?",
        "javob": "daryo",
        "maslahat": "Tabiatda uchraydi"
    },
    {
        "savol": "Yelkasida bir yuk ko'taradi, lekin charchamaydi. Nima bu?",
        "javob": "tog'",
        "maslahat": "Baland joyda joylashgan"
    },
    {
        "savol": "Kechasi tug'iladi, kunduz o'ladi. Nima bu?",
        "javob": "tun",
        "maslahat": "Qorong'u vaqt"
    },
    {
        "savol": "Bir oyog'i bor, lekin yura olmaydi. Nima bu?",
        "javob": "qo'ziqorin",
        "maslahat": "O'rmonda o'sadi"
    },
    {
        "savol": "Ichida suv bor, lekin dengiz emas. Nima bu?",
        "javob": "tarvuz",
        "maslahat": "Yozda yeyiladi"
    },
    {
        "savol": "Qanoti bor, lekin uchmaydigan narsa nima?",
        "javob": "eshik",
        "maslahat": "Uyda bor"
    },
]

# =============================================
# O'YIN HOLATLARI (FSM States)
# =============================================
class OyinHolati(StatesGroup):
    oyin_jarayonida = State()
    maslahat_kutish = State()

# =============================================
# FOYDALANUVCHI MA'LUMOTLARI (xotira)
# =============================================
user_stats = {}

def get_user_stats(user_id: int) -> dict:
    if user_id not in user_stats:
        user_stats[user_id] = {
            "jami": 0,
            "togri": 0,
            "noto_gri": 0,
            "streak": 0,
            "max_streak": 0
        }
    return user_stats[user_id]

# =============================================
# KLAVIATURA TUGMALARI
# =============================================
def bosh_menu_klaviatura():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎮 O'yin boshlash")],
            [KeyboardButton(text="📊 Natijalarim"), KeyboardButton(text="❓ Yordam")],
        ],
        resize_keyboard=True
    )

def oyin_klaviatura():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💡 Maslahat"), KeyboardButton(text="⏭ O'tkazib yuborish")],
            [KeyboardButton(text="🏠 Bosh menu")],
        ],
        resize_keyboard=True
    )

# =============================================
# /start BUYRUG'I
# =============================================
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    ism = message.from_user.first_name
    await message.answer(
        f"Salom, {ism}! 👋\n\n"
        "🧩 *Topishmoq Botiga* xush kelibsiz!\n\n"
        "Men sizga qiziqarli topishmoqlar beraman.\n"
        "Har bir to'g'ri javob uchun ball olasiz!\n\n"
        "Tayyor bo'lsangiz boshlaylik! 🚀",
        parse_mode="Markdown",
        reply_markup=bosh_menu_klaviatura()
    )

# =============================================
# O'YIN BOSHLASH
# =============================================
@dp.message(F.text == "🎮 O'yin boshlash")
async def oyin_boshlash(message: types.Message, state: FSMContext):
    topishmoq = random.choice(TOPISHMOQLAR)
    
    await state.set_state(OyinHolati.oyin_jarayonida)
    await state.update_data(
        topishmoq=topishmoq,
        urinishlar=0,
        maslahat_olindi=False
    )
    
    await message.answer(
        "🎯 *Yangi topishmoq!*\n\n"
        f"❓ {topishmoq['savol']}\n\n"
        "_Javobingizni yozing..._",
        parse_mode="Markdown",
        reply_markup=oyin_klaviatura()
    )

# =============================================
# MASLAHAT OLISH
# =============================================
@dp.message(F.text == "💡 Maslahat", OyinHolati.oyin_jarayonida)
async def maslahat_berish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    topishmoq = data["topishmoq"]
    
    await state.update_data(maslahat_olindi=True)
    await message.answer(
        f"💡 *Maslahat:* {topishmoq['maslahat']}\n\n"
        "Endi javob bera olasizmi? 🤔",
        parse_mode="Markdown"
    )

# =============================================
# O'TKAZIB YUBORISH
# =============================================
@dp.message(F.text == "⏭ O'tkazib yuborish", OyinHolati.oyin_jarayonida)
async def otkazib_yuborish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    topishmoq = data["topishmoq"]
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
    
    stats["jami"] += 1
    stats["noto_gri"] += 1
    stats["streak"] = 0
    
    yangi_topishmoq = random.choice(TOPISHMOQLAR)
    await state.update_data(
        topishmoq=yangi_topishmoq,
        urinishlar=0,
        maslahat_olindi=False
    )
    
    await message.answer(
        f"⏭ O'tkazib yubordingiz!\n\n"
        f"✅ *To'g'ri javob:* `{topishmoq['javob']}`\n\n"
        "━━━━━━━━━━━━━━━\n"
        f"🎯 *Keyingi topishmoq:*\n\n"
        f"❓ {yangi_topishmoq['savol']}\n\n"
        "_Javobingizni yozing..._",
        parse_mode="Markdown"
    )

# =============================================
# JAVOB TEKSHIRISH
# =============================================
@dp.message(OyinHolati.oyin_jarayonida)
async def javob_tekshirish(message: types.Message, state: FSMContext):
    # Tugmalarni e'tiborsiz qoldirish
    if message.text in ["🏠 Bosh menu", "📊 Natijalarim", "❓ Yordam"]:
        return
    
    data = await state.get_data()
    topishmoq = data["topishmoq"]
    maslahat_olindi = data.get("maslahat_olindi", False)
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
    
    foydalanuvchi_javobi = message.text.lower().strip()
    togri_javob = topishmoq["javob"].lower().strip()
    
    if foydalanuvchi_javobi == togri_javob:
        # To'g'ri javob
        stats["jami"] += 1
        stats["togri"] += 1
        stats["streak"] += 1
        if stats["streak"] > stats["max_streak"]:
            stats["max_streak"] = stats["streak"]
        
        ball = 1 if maslahat_olindi else 2
        
        # Yangi topishmoq
        yangi_topishmoq = random.choice(TOPISHMOQLAR)
        await state.update_data(
            topishmoq=yangi_topishmoq,
            urinishlar=0,
            maslahat_olindi=False
        )
        
        streak_msg = f"🔥 Ketma-ket: {stats['streak']}" if stats["streak"] > 1 else ""
        
        await message.answer(
            f"✅ *To'g'ri!* Tabriklaymiz! 🎉\n"
            f"💰 +{ball} ball {'(maslahat olindi)' if maslahat_olindi else ''}\n"
            f"{streak_msg}\n\n"
            "━━━━━━━━━━━━━━━\n"
            f"🎯 *Keyingi topishmoq:*\n\n"
            f"❓ {yangi_topishmoq['savol']}\n\n"
            "_Javobingizni yozing..._",
            parse_mode="Markdown"
        )
    else:
        # Noto'g'ri javob
        urinishlar = data.get("urinishlar", 0) + 1
        await state.update_data(urinishlar=urinishlar)
        
        if urinishlar >= 3:
            # 3 urinishdan keyin javobni ko'rsat
            stats["jami"] += 1
            stats["noto_gri"] += 1
            stats["streak"] = 0
            
            yangi_topishmoq = random.choice(TOPISHMOQLAR)
            await state.update_data(
                topishmoq=yangi_topishmoq,
                urinishlar=0,
                maslahat_olindi=False
            )
            
            await message.answer(
                f"❌ 3 urinish tugadi!\n\n"
                f"✅ *To'g'ri javob:* `{topishmoq['javob']}`\n\n"
                "━━━━━━━━━━━━━━━\n"
                f"🎯 *Keyingi topishmoq:*\n\n"
                f"❓ {yangi_topishmoq['savol']}\n\n"
                "_Javobingizni yozing..._",
                parse_mode="Markdown"
            )
        else:
            qolgan = 3 - urinishlar
            await message.answer(
                f"❌ Noto'g'ri! Yana urinib ko'ring.\n"
                f"📝 Qolgan urinish: {qolgan}\n\n"
                "💡 Maslahat olishingiz mumkin!",
                parse_mode="Markdown"
            )

# =============================================
# NATIJALAR
# =============================================
@dp.message(F.text == "📊 Natijalarim")
async def natijalar(message: types.Message):
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
    
    if stats["jami"] == 0:
        await message.answer(
            "📊 Hali o'yin o'ynamadingiz!\n"
            "🎮 O'yin boshlash tugmasini bosing.",
            reply_markup=bosh_menu_klaviatura()
        )
        return
    
    foiz = round(stats["togri"] / stats["jami"] * 100) if stats["jami"] > 0 else 0
    
    await message.answer(
        f"📊 *Sizning natijalaringiz:*\n\n"
        f"🎯 Jami topishmoq: {stats['jami']}\n"
        f"✅ To'g'ri javoblar: {stats['togri']}\n"
        f"❌ Noto'g'ri javoblar: {stats['noto_gri']}\n"
        f"📈 Foiz: {foiz}%\n"
        f"🔥 Eng yaxshi ketma-ket: {stats['max_streak']}\n"
        f"⚡ Hozirgi ketma-ket: {stats['streak']}",
        parse_mode="Markdown",
        reply_markup=bosh_menu_klaviatura()
    )

# =============================================
# YORDAM
# =============================================
@dp.message(F.text == "❓ Yordam")
async def yordam(message: types.Message):
    await message.answer(
        "❓ *Yordam*\n\n"
        "🎮 *O'yin boshlash* - Yangi topishmoq olish\n"
        "💡 *Maslahat* - Topishmoq uchun yordam\n"
        "⏭ *O'tkazib yuborish* - Keyingi topishmoqqa o'tish\n"
        "📊 *Natijalarim* - O'yin statistikasi\n\n"
        "📌 *Qoidalar:*\n"
        "• Maslahat olmay to'g'ri javob = 2 ball\n"
        "• Maslahat olib to'g'ri javob = 1 ball\n"
        "• 3 urinishdan keyin javob ko'rsatiladi\n\n"
        "Omad! 🍀",
        parse_mode="Markdown",
        reply_markup=bosh_menu_klaviatura()
    )

# =============================================
# BOSH MENUGA QAYTISH
# =============================================
@dp.message(F.text == "🏠 Bosh menu")
async def bosh_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Bosh menuga qaytdingiz!",
        reply_markup=bosh_menu_klaviatura()
    )

# =============================================
# BOTNI ISHGA TUSHIRISH
# =============================================
async def main():
    print("🤖 Topishmoq boti ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
