"""
Translations
============
All bot text translations in Russian and Uzbek
"""

TRANSLATIONS = {
    'ru': {
        # Language selection
        'choose_language': 'Выберите язык / Tilni tanlang 🌐',
        
        # Service selection
        'choose_service': 'Какую услугу вы хотите заказать? 🧹',
        'carpet_cleaning': '🧺 Чистка ковров',
        'sofa_cleaning': '🛋 Чистка мебели',
        'back_to_language': '⬅️ Изменить язык',
        
        # Service descriptions
        'carpet_description': '''🧺 <b>ХИМЧИСТКА КОВРОВ</b>

━━━━━━━━━━━━━━━━━━━━━
✅ <b>Что входит в услугу:</b>

🔹 Глубокая профессиональная чистка
🔹 Удаление любых пятен и запахов
🔹 Бесплатный самовывоз и доставка
🔹 Безопасные немецкие средства
🔹 Профессиональная сушка
🔹 Упаковка и защита

━━━━━━━━━━━━━━━━━━━━━
💰 Стоимость: от 15,000 сум/м²
⏱ Срок выполнения: 1-2 дня
🎁 Скидка 10% при заказе от 3 ковров

📞 Остались вопросы? Позвоните нам!
+998 90 123-45-67''',
        
        'sofa_description': '''🛋 <b>ЧИСТКА МЕБЕЛИ</b>

━━━━━━━━━━━━━━━━━━━━━
✅ <b>Что входит в услугу:</b>

🔹 Глубокая чистка обивки
🔹 Удаление пятен и неприятных запахов
🔹 Защитная пропитка ткани
🔹 Безопасные гипоаллергенные средства
🔹 Быстрая сушка

━━━━━━━━━━━━━━━━━━━━━
💰 Стоимость:
   • 2-местный диван: от 50,000 сум
   • 3-местный диван: от 70,000 сум
   • Угловой диван: от 90,000 сум
   • Кресло: от 30,000 сум

⏱ Срок выполнения: 1 день

📞 +998 90 123-45-67''',
        
        # Buttons
        'order_now': '📦 Заказать сейчас',
        'back': '⬅️ Назад',
        
        # Quantity
        'select_quantity': 'Сколько ковров нужно почистить? 🧮',
        'select_quantity_sofa': 'Сколько предметов нужно почистить? 🧮',
        'enter_custom_quantity': 'Введите точное количество (от 6 до 10):',
        
        # Size
        'select_size_carpet': 'Выберите размер {number}-го ковра 📏\n\n({current} из {total})',
        'select_size_sofa': 'Выберите тип {number}-й мебели 🛋\n\n({current} из {total})',
        'custom_size': '✍️ Другой размер',
        'enter_custom_size': 'Введите размер в формате ШxД (например: 2.5x3):',
        
        # Address
        'enter_address': 'Укажите адрес для самовывоза 📍',
        'address_manual': '✍️ Ввести адрес вручную',
        'address_location': '📍 Отправить геолокацию',
        'address_manual_prompt': 'Напишите ваш адрес\n\nПример: Ташкент, Мирабадский район, ул. Лабзак, дом 5',
        'location_request': '📍 Нажмите кнопку ниже, чтобы поделиться локацией',
        
        # Name
        'enter_name': '''Как вас зовут? 👤

Пожалуйста, укажите ваше полное имя

<i>Пример: Шавкат Шокиров</i>''',
        
        # Phone
        'enter_phone': '''Укажите ваш номер телефона 📱

Мы позвоним вам для подтверждения заказа

<i>Формат: +998 XX XXX-XX-XX
Пример: +998 90 123-45-67</i>''',
        
        'share_contact': '📱 Поделиться номером',
        'enter_manually': '✍️ Ввести вручную',
        
        # Thank you
        'thank_you': 'Спасибо! ❤️',
        
        # Order summary
        'add_comment': '💬 Добавить комментарий',
        'confirm_order': '✅ Подтвердить заказ',
        'new_order': '🔄 Новый заказ',
        'edit_order': '✏️ Редактировать',
        'contact_admin': '👨‍💼 Связаться с оператором',
        
        # Comment
        'comment_prompt': '''💬 <b>Добавьте комментарий к заказу</b>

Например:
- Позвоните заранее
- Домофон не работает
- Есть собака во дворе
- Другие пожелания

Напишите ваш комментарий:''',
        
        # Order confirmed
        'order_confirmed': '''✅ <b>ЗАКАЗ УСПЕШНО СОЗДАН!</b>

Номер вашего заказа: <b>#{order_number}</b>

Наш оператор свяжется с вами в ближайшее время для уточнения деталей.

Ожидайте звонка! 📞

Вы можете отслеживать статус заказа в разделе "Мои заказы"''',
        
        # Feedback
        'rate_service': 'Мы будем рады вашему отзыву! ⭐\n\nПожалуйста, оцените нашу работу:',
        'feedback_thanks': 'Спасибо за оценку! {stars}\n\nРасскажите, что вам понравилось или что можно улучшить?\n\nВаш отзыв поможет нам стать лучше! 💙',
        'write_feedback': '✍️ Написать отзыв',
        'skip_feedback': '⏭ Пропустить',
        'write_feedback_prompt': 'Напишите ваш отзыв:',
        
        # Thank you after feedback
        'feedback_complete': '''🙏 <b>БОЛЬШОЕ СПАСИБО!</b>

Ваш отзыв очень важен для нас!

Будем рады видеть вас снова! ❤️

━━━━━━━━━━━━━━━━━━━━━
Нужна чистка снова?''',
        
        # My orders
        'my_orders_title': '📋 <b>МОИ ЗАКАЗЫ</b>',
        'no_orders': '''📋 <b>МОИ ЗАКАЗЫ</b>

У вас пока нет заказов.

Оформите первый заказ прямо сейчас!''',
        
        # Errors
        'error_invalid_phone': '❌ Неверный формат номера. Пожалуйста, используйте формат: +998XXXXXXXXX',
        'error_invalid_name': '❌ Имя должно содержать минимум 5 символов',
        'error_invalid_comment': '❌ Комментарий слишком длинный (максимум 500 символов)',
        'error_generic': '❌ Произошла ошибка. Пожалуйста, попробуйте позже.',
    },
    
    'uz': {
        # Language selection
        'choose_language': 'Выберите язык / Tilni tanlang 🌐',
        
        # Service selection
        'choose_service': 'Qaysi xizmatni buyurtma qilmoqchisiz? 🧹',
        'carpet_cleaning': '🧺 Gilam tozalash',
        'sofa_cleaning': '🛋 Mebel tozalash',
        'back_to_language': "⬅️ Tilni o'zgartirish",
        
        # Service descriptions
        'carpet_description': '''🧺 <b>GILAM KIMYOVIY TOZALASH</b>

━━━━━━━━━━━━━━━━━━━━━
✅ <b>Xizmat tarkibi:</b>

🔹 Chuqur professional tozalash
🔹 Har qanday dog' va hidni olib tashlash
🔹 Bepul olib ketish va yetkazib berish
🔹 Xavfsiz nemis vositalari
🔹 Professional quritish
🔹 Qadoqlash va himoya

━━━━━━━━━━━━━━━━━━━━━
💰 Narx: 15,000 so'mdan/m²
⏱ Bajarish muddati: 1-2 kun
🎁 3 ta gilamdan ortiq bo'lsa 10% chegirma

📞 Savol bormi? Qo'ng'iroq qiling!
+998 90 123-45-67''',
        
        'sofa_description': '''🛋 <b>MEBEL TOZALASH</b>

━━━━━━━━━━━━━━━━━━━━━
✅ <b>Xizmat tarkibi:</b>

🔹 Qoplamani chuqur tozalash
🔹 Dog'lar va yomon hidlarni olib tashlash
🔹 Matoni himoya qilish
🔹 Xavfsiz gipoallergen vositalar
🔹 Tez quritish

━━━━━━━━━━━━━━━━━━━━━
💰 Narx:
   • 2 o'rindiqli divan: 50,000 so'mdan
   • 3 o'rindiqli divan: 70,000 so'mdan
   • Burchakli divan: 90,000 so'mdan
   • Kreslo: 30,000 so'mdan

⏱ Bajarish muddati: 1 kun

📞 +998 90 123-45-67''',
        
        # Buttons
        'order_now': '📦 Buyurtma berish',
        'back': '⬅️ Orqaga',
        
        # Quantity
        'select_quantity': 'Nechta gilam tozalash kerak? 🧮',
        'select_quantity_sofa': 'Nechta mebel tozalash kerak? 🧮',
        'enter_custom_quantity': 'Aniq sonini kiriting (6 dan 10 gacha):',
        
        # Size
        'select_size_carpet': "{number}-gilam o'lchamini tanlang 📏\n\n({current} dan {total})",
        'select_size_sofa': "{number}-mebel turini tanlang 🛋\n\n({current} dan {total})",
        'custom_size': "✍️ Boshqa o'lcham",
        'enter_custom_size': "O'lchamni EnixBo'yi formatida kiriting (masalan: 2.5x3):",
        
        # Address
        'enter_address': 'Olib ketish manzilini kiriting 📍',
        'address_manual': "✍️ Qo'lda kiritish",
        'address_location': '📍 Joylashuv yuborish',
        'address_manual_prompt': "Manzilingizni yozing\n\nMisol: Toshkent, Mirabad tumani, Labzak ko'chasi, 5-uy",
        'location_request': "📍 Joylashuvni ulashish uchun quyidagi tugmani bosing",
        
        # Name
        'enter_name': '''Ismingiz nima? 👤

Iltimos, to'liq ismingizni kiriting

<i>Misol: Shavkat Shokirov</i>''',
        
        # Phone
        'enter_phone': '''Telefon raqamingizni kiriting 📱

Buyurtmani tasdiqlash uchun qo'ng'iroq qilamiz

<i>Format: +998 XX XXX-XX-XX
Misol: +998 90 123-45-67</i>''',
        
        'share_contact': '📱 Raqamni ulashish',
        'enter_manually': "✍️ Qo'lda kiritish",
        
        # Thank you
        'thank_you': 'Rahmat! ❤️',
        
        # Order summary
        'add_comment': "💬 Izoh qo'shish",
        'confirm_order': '✅ Tasdiqlash',
        'new_order': '🔄 Yangi buyurtma',
        'edit_order': '✏️ Tahrirlash',
        'contact_admin': "👨‍💼 Operator bilan bog'lanish",
        
        # Comment
        'comment_prompt': '''💬 <b>Buyurtmaga izoh qo'shing</b>

Masalan:
- Oldindan qo'ng'iroq qiling
- Domofon ishlamaydi
- Hovlida it bor
- Boshqa xohishlar

Izohingizni yozing:''',
        
        # Order confirmed
        'order_confirmed': '''✅ <b>BUYURTMA MUVAFFAQIYATLI YARATILDI!</b>

Buyurtma raqamingiz: <b>#{order_number}</b>

Operatorimiz tez orada siz bilan bog'lanadi.

Qo'ng'iroqni kuting! 📞

Buyurtma holatini "Mening buyurtmalarim" bo'limida kuzatishingiz mumkin''',
        
        # Feedback
        'rate_service': "Fikr-mulohazangizni kutamiz! ⭐\n\nIltimos, xizmatimizni baholang:",
        'feedback_thanks': "Baho uchun rahmat! {stars}\n\nNimalar yoqdingiz yoki nimani yaxshilash mumkin?\n\nFikringiz bizga yordam beradi! 💙",
        'write_feedback': '✍️ Izoh yozish',
        'skip_feedback': "⏭ O'tkazib yuborish",
        'write_feedback_prompt': 'Izohingizni yozing:',
        
        # Thank you after feedback
        'feedback_complete': '''🙏 <b>KATTA RAHMAT!</b>

Fikr-mulohazangiz biz uchun juda muhim!

Sizni yana ko'rishdan xursandmiz! ❤️

━━━━━━━━━━━━━━━━━━━━━
Yana tozalash kerakmi?''',
        
        # My orders
        'my_orders_title': '📋 <b>MENING BUYURTMALARIM</b>',
        'no_orders': '''📋 <b>MENING BUYURTMALARIM</b>

Sizda hali buyurtmalar yo'q.

Birinchi buyurtmani hozir bering!''',
        
        # Errors
        'error_invalid_phone': "❌ Noto'g'ri format. Iltimos, +998XXXXXXXXX formatidan foydalaning",
        'error_invalid_name': "❌ Ism kamida 5 ta belgidan iborat bo'lishi kerak",
        'error_invalid_comment': '❌ Izoh juda uzun (maksimal 500 ta belgi)',
        'error_generic': "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
    }
}


def get_text(language: str, key: str, **kwargs) -> str:
    """
    Get translated text with optional formatting
    
    Args:
        language: Language code ('ru' or 'uz')
        key: Translation key
        **kwargs: Format arguments
        
    Returns:
        Translated and formatted text
    """
    # Get translation, default to Russian if language not found
    text = TRANSLATIONS.get(language, TRANSLATIONS['ru']).get(key, key)
    
    # Format with kwargs if provided
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text