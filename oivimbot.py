import telebot as _t_b
from telebot import types as _t_p
import os
import io
import urllib.parse
from threading import Thread
from flask import Flask

# Flask app taaki Render ka port requirement pura ho jaye
app = Flask('')

@app.route('/')
def home():
    return "Oivim Middleman Bot is Alive!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_web)
    t.start()

try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

_T_K = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')          
_UPI_ID = os.getenv('UPI_ID', 'yourupiid@upi') 
_A_I = 8904326919                   

_b_t = _t_b.TeleBot(_T_K)

_t_d = {}
_t_c = 1
_e_a = set()
_b_s = {
    "total_deals": 0,
    "successful_deals": 0,
    "canceled_deals": 0,
    "vouches_count": 0
}

def _calculate_fee(_amt):
    if _amt <= 100: return 15
    elif _amt <= 200: return 20
    elif _amt <= 300: return 25
    elif _amt <= 400: return 30
    elif _amt <= 500: return 35
    elif _amt <= 600: return 40
    elif _amt <= 700: return 45
    elif _amt <= 800: return 50
    elif _amt <= 900: return 55
    elif _amt <= 1000: return 55
    elif _amt <= 1500: return 80
    elif _amt <= 2000: return 105
    elif _amt <= 2500: return 130
    elif _amt <= 3000: return 155
    elif _amt <= 4000: return 205
    elif _amt <= 5000: return 255
    elif _amt <= 6000: return 305
    elif _amt <= 7000: return 355
    elif _amt <= 8000: return 405
    elif _amt <= 9000: return 455
    elif _amt <= 10000: return 505
    else:
        return int(_amt * 0.05)

def _generate_qr_stream(upi_uri):
    if HAS_QR:
        img = qrcode.make(upi_uri)
        bio = io.BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0)
        return bio
    else:
        return f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(upi_uri)}"

# 1. CALC & DYNAMIC QR GENERATOR
@_b_t.message_handler(commands=['calc', 'pay'])
def _h_calc(_m_g):
    _text_clean = _m_g.text.split('@')[0]
    _a_s = _text_clean.split()
    if len(_a_s) < 2:
        _b_t.reply_to(_m_g, "⚠️ Sahi format use kar: `/calc <Deal_Amount>`\nMisal ke taur par: `/calc 500`", parse_mode='Markdown')
        return
    
    try:
        _amt = float(_a_s[1])
        _fee = _calculate_fee(_amt)
        _total_pay = _amt + _fee
        
        _upi_link = f"upi://pay?pa={_UPI_ID}&pn=Oivim%20MM&am={_total_pay:.2f}&cu=INR"
        
        _calc_msg = (
            f"⚡ **OFFICIAL PAYMENT QR CODE**\n"
            f"__________________________________________________\n\n"
            f"• **Deal Amount:** ₹{_amt:,.2f}\n"
            f"• **MM Fee:** ₹{_fee}\n"
            f"• **Total Payable Amount:** ₹{_total_pay:,.2f} ✅\n\n"
            f"👉 *Kripya uper diye gaye QR code ko scan karke exact **₹{_total_pay:,.2f}** pay karein.* \n\n"
            f"👤 Official MM: @oivim"
        )
        
        _qr_img = _generate_qr_stream(_upi_link)
        _b_t.send_photo(_m_g.chat.id, photo=_qr_img, caption=_calc_msg, parse_mode='Markdown')
        
    except ValueError:
        _b_t.reply_to(_m_g, "⚠️ Kripya valid amount daalein (Jaise: `/calc 500`)", parse_mode='Markdown')

# 2. START & HELP
@_b_t.message_handler(commands=['start', 'help'])
def _h_s(_m_g):
    _w_t = (
        "WELCOME TO OIVIM MIDDLEMAN\n\n"
        "Welcome to our trusted Middleman Service.\n\n"
        "• Secure Deal Handling\n"
        "• Payment Verification\n"
        "• Fair Transactions\n"
        "• Professional Support\n\n"
        "Please read /rules before starting.\n\n"
        "Fees: /fees\n"
        "Auto Fee & QR Generator: /calc <Amount>\n"
        "Deal Form: /form\n"
        "Vouch: /vouch\n"
        "QR Code: /qr\n"
        "New Trade: /newtrade\n"
        "My Trades: /mytrades\n"
        "Stats: /stats\n"
        "Cancel Deal: /cancel\n"
        "Dispute: /dispute\n\n"
        "Official MM: @oivim"
    )
    _b_t.send_message(_m_g.chat.id, _w_t, parse_mode='Markdown')

# 3. ADMIN PANEL
@_b_t.message_handler(commands=['admin'])
def _h_admin_panel(_m_g):
    _admin_text = (
        "👑 **ADMIN CONTROL PANEL**\n\n"
        "Admin commands list:\n"
        "• `/received` - Payment receive hone par\n"
        "• `/release` - Deal successful karne ke liye\n"
        "• `/cancel <ID>` - Deal cancel karne ke liye\n"
        "• `/calc <Amount>` - Dynamic QR + Fees generate karne ke liye\n"
        "• `/broadcast <message>` - Sabhi ko message bhejne ke liye"
    )
    _b_t.reply_to(_m_g, _admin_text, parse_mode='Markdown')

# 4. FORM
@_b_t.message_handler(commands=['form'])
def _h_f(_m_g):
    _f_t = (
        "📝 **MIDDLEMAN DEAL FORM**\n\n"
        "👤 Buyer:\n"
        "👤 Seller:\n"
        "📦 Deal Details:\n"
        "💰 Deal Amount:\n"
        "💳 Payment Method:\n\n"
        "Please provide correct details before starting the deal.\n\n"
        "👤 Official MM: @oivim"
    )
    _b_t.reply_to(_m_g, _f_t, parse_mode='Markdown')

# 5. NEW TRADE
@_b_t.message_handler(commands=['newtrade'])
def _h_n(_m_g):
    global _t_c
    _text_clean = _m_g.text.split('@')[0]
    _a_s = _text_clean.split(maxsplit=2)
    
    if len(_a_s) < 3:
        _b_t.reply_to(_m_g, "⚠️ Sahi format use kar:\n`/newtrade <Item Name> <Price>`", parse_mode='Markdown')
        return

    _i_n = _a_s[1]
    _p_c = _a_s[2]
    _t_i = _t_c
    _t_c += 1

    _t_d[_t_i] = {
        "item": _i_n,
        "price": _p_c,
        "seller": _m_g.from_user.username or _m_g.from_user.first_name,
        "buyer": None,
        "status": "Waiting for Buyer"
    }

    _b_s["total_deals"] += 1

    _m_p = _t_p.InlineKeyboardMarkup()
    _j_b = _t_p.InlineKeyboardButton("🤝 Join Trade as Buyer", callback_data=f"join_{_t_i}")
    _m_p.add(_j_b)

    _r_s = (
        f"⚡ **DEAL INITIATED** (ID: #{_t_i})\n"
        f"__________________________________________________\n\n"
        f"• **Item:** {_i_n}\n"
        f"• **Price:** {_p_c}\n"
        f"• **Seller:** @{_t_d[_t_i]['seller']}\n"
        f"• **Status:** {_t_d[_t_i]['status']}\n"
    )
    
    _b_t.send_message(_m_g.chat.id, _r_s, reply_markup=_m_p, parse_mode='Markdown')

@_b_t.callback_query_handler(func=lambda c: c.data.startswith('join_'))
def _h_j(c):
    _t_i = int(c.data.split('_')[1])
    
    if _t_i not in _t_d:
        _b_t.answer_callback_query(c.id, "Yeh deal khatam ho chuki hai ya exist nahi karti.")
        return

    _t_v = _t_d[_t_i]
    
    if _t_v["buyer"] is not None:
        _b_t.answer_callback_query(c.id, "Pehle hi buyer aa chuka hai is deal mein!")
        return

    _b_n = c.from_user.username or c.from_user.first_name
    _t_v["buyer"] = _b_n
    _t_v["status"] = "Payment Pending"

    _u_t = (
        f"🔒 **ESCROW LOCKED** (ID: #{_t_i})\n"
        f"__________________________________________________\n\n"
        f"• **Item:** {_t_v['item']}\n"
        f"• **Price:** {_t_v['price']}\n"
        f"• **Seller:** @{_t_v['seller']}\n"
        f"• **Buyer:** @{_b_n}\n"
        f"• **Status:** {_t_v['status']}\n\n"
        f"👉 *Buyer chupchap payment bhej aur screenshot seedha admin ko de.*"
    )

    _b_t.edit_message_text(_u_t, c.message.chat.id, c.message.message_id, parse_mode='Markdown')
    _b_t.answer_callback_query(c.id, "Badhai ho, tune trade join kar li hai.")

# 6. RECEIVED
@_b_t.message_handler(commands=['received', 'receive'])
def _h_received(_m_g):
    _c_t = (
        "📥 **PAYMENT RECEIVED**\n\n"
        "Payment has been received. Verification is currently in progress.\n\n"
        "Please wait for official confirmation before proceeding.\n\n"
        "👤 Middleman: @oivim\n\n"
        "⚠️ Do not release any asset without final confirmation."
    )
    _b_t.send_message(_m_g.chat.id, _c_t, parse_mode='Markdown')

# 7. RELEASE
@_b_t.message_handler(commands=['release', 'realse'])
def _h_release(_m_g):
    _t_d.clear()
    _b_s["successful_deals"] += 1
    _b_s["vouches_count"] += 1  

    _l_t = (
        "✅ **DEAL RELEASED**\n\n"
        "Both parties ki verification successfully complete ho gayi hai.\n\n"
        "Transaction officially completed!\n\n"
        "Thank you for using our Middleman Service.\n\n"
        "👤 MM: @oivim"
    )
    _b_t.send_message(_m_g.chat.id, _l_t, parse_mode='Markdown')

# 8. CANCEL
@_b_t.message_handler(commands=['cancel'])
def _h_e(_m_g):
    _text_clean = _m_g.text.split('@')[0]
    _a_s = _text_clean.split()
    if len(_a_s) < 2:
        _b_t.reply_to(_m_g, "⚠️ Sahi format use kar: `/cancel <Trade_ID>`", parse_mode='Markdown')
        return
    
    try:
        _t_i = int(_a_s[1])
    except ValueError:
        _b_t.reply_to(_m_g, "⚠️ Valid Trade ID daal.", parse_mode='Markdown')
        return

    if _t_i in _t_d:
        del _t_d[_t_i]
        _b_s["canceled_deals"] += 1
        _b_t.reply_to(_m_g, f"❌ Deal `#{_t_i}` radd kar di gayi hai.", parse_mode='Markdown')
    else:
        _b_t.reply_to(_m_g, "⚠️ Yeh Trade ID nahi mili database mein.")

# 9. STATS
@_b_t.message_handler(commands=['stats'])
def _h_s_t(_m_g):
    _s_t = (
        "📊 **BOT STATISTICS & RECORDS**\n"
        "__________________________________________________\n\n"
        f"• Total Deals Created: `{_b_s['total_deals']}`\n"
        f"• Successful Deals: `{_b_s['successful_deals']}` ✅\n"
        f"• Canceled Deals: `{_b_s['canceled_deals']}` ❌\n"
        f"• Total Vouches Collected: `{_b_s['vouches_count']}` ⭐\n"
        f"• Active Deals Right Now: `{len(_t_d)}` 🔄"
    )
    _b_t.reply_to(_m_g, _s_t, parse_mode='Markdown')

# 10. DISPUTE
@_b_t.message_handler(commands=['dispute'])
def _h_d(_m_g):
    _text_clean = _m_g.text.split('@')[0]
    _a_s = _text_clean.split()
    if len(_a_s) < 2:
        _b_t.reply_to(_m_g, "⚠️ Format: `/dispute <Trade_ID>`", parse_mode='Markdown')
        return
    
    _t_i = _a_s[1]
    _d_t = (
        f"🚨 **DISPUTE RAISED** (ID: #{_t_i})\n"
        f"__________________________________________________\n\n"
        f"⚠️ Scam ki koshish mat karna kisi ne bhi!\n"
        f"🛑 Sabhi log chup chap baitho, @oivim handle kar raha hai."
    )
    _b_t.send_message(_m_g.chat.id, _d_t, parse_mode='Markdown')

# 11. FEES
@_b_t.message_handler(commands=['fees'])
def _h_f_s(_m_g):
    _f_s = (
        "MIDDLEMAN FEES LIST\n\n"
        "₹100 Deal — ₹15\n"
        "₹200 Deal — ₹20\n"
        "₹300 Deal — ₹25\n"
        "₹400 Deal — ₹30\n"
        "₹500 Deal — ₹35\n"
        "₹600 Deal — ₹40\n"
        "₹700 Deal — ₹45\n"
        "₹800 Deal — ₹50\n"
        "₹900 Deal — ₹55\n"
        "₹1,000 Deal — ₹55\n"
        "₹1,500 Deal — ₹80\n"
        "₹2,000 Deal — ₹105\n"
        "₹2,500 Deal — ₹130\n"
        "₹3,000 Deal — ₹155\n"
        "₹4,000 Deal — ₹205\n"
        "₹5,000 Deal — ₹255\n"
        "₹6,000 Deal — ₹305\n"
        "₹7,000 Deal — ₹355\n"
        "₹8,000 Deal — ₹405\n"
        "₹9,000 Deal — ₹455\n"
        "₹10,000 Deal — ₹505\n\n"
        "Official MM: @oivim"
    )
    _b_t.reply_to(_m_g, _f_s, parse_mode='Markdown')

# 12. RULES
@_b_t.message_handler(commands=['rules'])
def _h_ru(_m_g):
    _r_t = (
        "📜 MIDDLEMAN RULES\n\n"
        "1. Sirf official ID @oivim par trust karein.\n"
        "2. Payment verification se pehle asset transfer na karein.\n"
        "3. Fake payment receipts strictly prohibited hain.\n"
        "4. Deal mein respect aur discipline maintain karein.\n"
        "5. Har transaction mein proper verification mandatory hai.\n\n"
        "⚠️ Stay Safe | Trade Smart"
    )
    _b_t.reply_to(_m_g, _r_t, parse_mode='Markdown')

# 13. VOUCH
@_b_t.message_handler(commands=['vouch'])
def _h_v(_m_g):
    _h_t = (
        "⭐ **VOUCH CONFIRMATION**\n\n"
        "Deal successfully completed!\n"
        "Please Drop Vouch below:"
    )
    _b_t.send_message(_m_g.chat.id, _h_t, parse_mode='Markdown')
    
    _v_o = "I Vouch @oivim For MM'D"
    _b_t.send_message(_m_g.chat.id, f"```text\n{_v_o}\n```", parse_mode='Markdown')

# 14. QR STATIC
@_b_t.message_handler(commands=['qr'])
def _h_q(_m_g):
    _upi_link = f"upi://pay?pa={_UPI_ID}&pn=Oivim%20MM&cu=INR"
    _q_c = (
        "⚡ **OFFICIAL PAYMENT QR CODE**\n\n"
        "Scan and pay using any UPI app.\n"
        "👤 Official MM: @oivim"
    )
    _qr_img = _generate_qr_stream(_upi_link)
    _b_t.send_photo(_m_g.chat.id, photo=_qr_img, caption=_q_c, parse_mode='Markdown')

# 15. MY TRADES
@_b_t.message_handler(commands=['mytrades'])
def _h_m(_m_g):
    if not _t_d:
        _b_t.reply_to(_m_g, "📭 Abhi market bilkul thandi hai, ek bhi active deal nahi chal rahi.", parse_mode='Markdown')
        return
    
    _t_x = f"📋 **CHAL RAHI ACTIVE DEALS:**\n\n"
    for _t_i, _t_v in _t_d.items():
        _t_x += f"🔹 `#{_t_i}` | {_t_v['item']} | {_t_v['status']}\n"
    
    _b_t.reply_to(_m_g, _t_x, parse_mode='Markdown')

# 16. BROADCAST
@_b_t.message_handler(commands=['broadcast'])
def _h_b(_m_g):
    _text_clean = _m_g.text.replace('/broadcast', '').split('@')[0].strip()
    _m_b = _text_clean
    if not _m_b:
        _b_t.reply_to(_m_g, "⚠️ Message toh likh kuch: `/broadcast <aapka message>`", parse_mode='Markdown')
        return
    
    _b_t.reply_to(_m_g, f"📢 **BROADCASTED:**\n\n{_m_b}", parse_mode='Markdown')

if __name__ == "__main__":
    keep_alive()
    print("Oivim Middleman Bot is online with Web Server...")
    _b_t.infinity_polling()
        
