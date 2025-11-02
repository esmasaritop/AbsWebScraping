from playwright.sync_api import sync_playwright

url = "https://abs.firat.edu.tr/tr/units"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)
    page.wait_for_timeout(5000)

    # Fakülte bloklarını bul
    faculties = page.query_selector_all(".toggle")

    for faculty in faculties:
        faculty_name = faculty.query_selector(".title-name").inner_text().strip()

        # 🎯 Sadece Teknoloji Fakültesi içindeki bölümleri kontrol et
        if "TEKNOLOJİ FAKÜLTESİ" in faculty_name.upper():
            print(f"🏛️ Fakülte bulundu: {faculty_name}\n")

            # Bu fakültenin altındaki tüm alt birimleri bul
            sub_departments = faculty.query_selector_all(".toggle")

            for dep in sub_departments:
                dep_title = dep.query_selector(".title-name").inner_text().strip()
                if dep_title.upper() == "YAZILIM MÜHENDİSLİĞİ":
                    print("📘 TEKNOLOJİ FAKÜLTESİ / YAZILIM MÜHENDİSLİĞİ AKADEMİSYENLERİ\n")
                    academics = dep.query_selector_all(".academicianjs")

                    for a in academics:
                        name = a.query_selector("p").inner_text().strip()
                        link = a.query_selector("a").get_attribute("href")
                        img = a.query_selector("img").get_attribute("src")

                        print("👨‍🏫 İsim:", name)
                        print("🔗 Profil:", link)
                        print("🖼️ Fotoğraf:", img)
                        print("-" * 50)
                    break

    browser.close()
