from playwright.sync_api import sync_playwright

# -----------------------------
# 1️⃣ Kullanıcıdan fakülte ve bölüm al
# -----------------------------
faculty_input = input("Fakülte adı: ").strip().upper()
department_input = input("Bölüm adı: ").strip().upper()

url = "https://abs.firat.edu.tr/tr/units"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)
    page.wait_for_timeout(5000)  # JS'nin yüklenmesi için

    # Fakülte bloklarını bul
    faculties = page.query_selector_all(".toggle")

    found = False
    for faculty in faculties:
        faculty_name = faculty.query_selector(".title-name").inner_text().strip().upper()

        if faculty_input in faculty_name:
            # Bu fakültenin altındaki bölümler
            sub_departments = faculty.query_selector_all(".toggle")

            for dep in sub_departments:
                dep_title = dep.query_selector(".title-name").inner_text().strip().upper()
                if department_input == dep_title:
                    academics = dep.query_selector_all(".academicianjs")
                    print(f"\n📘 {faculty_name} / {dep_title} AKADEMİSYENLERİ\n")

                    for a in academics:
                        name = a.query_selector("p").inner_text().strip()
                        link = a.query_selector("a").get_attribute("href")
                        img = a.query_selector("img").get_attribute("src")

                        print("👨‍🏫 İsim:", name)
                        print("🔗 Profil:", link)
                        print("🖼️ Fotoğraf:", img)
                        print("-" * 50)

                    found = True
                    break
            if found:
                break

    if not found:
        print("❌ Belirtilen fakülte veya bölüm bulunamadı!")

    browser.close()
