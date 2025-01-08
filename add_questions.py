from app import app, db, Quiz
import logging

logger = logging.getLogger(__name__)

def add_sample_questions():
    questions_data = {
        "python": [
            ("Was ist Python?", "Eine universelle, interpretierte Programmiersprache", ["Eine Programmiersprache für wissenschaftliches Rechnen", "Ein Webframework für Datenbanken", "Eine Datenvisualisierungsbibliothek"]),
            ("Was ist der Vorteil von Python im Vergleich zu Java?", "Einfacherer und kürzerer Code", ["Schnellere Ausführungsgeschwindigkeit", "Bessere Unterstützung für parallele Programmierung", "Höhere Stabilität"]),
            ("Welches Symbol wird in Python für Kommentare verwendet?", "#", ["//", "/* */", "<!-- -->"]),
            ("Welche der folgenden Datentypen gibt es in Python?", "list", ["table", "matrix", "arraylist"]),
            ("Welcher Operator wird für die Verkettung von Strings verwendet?", "+", ["-", "*", "/"]),
            ("Welche Schleife wird in Python verwendet, um eine Sequenz zu durchlaufen?", "for", ["while-do", "do-while", "foreach"]),
            ("Was bedeutet `None` in Python?", "Eine spezielle Konstante, die nichts darstellt", ["Ein leerer String", "Ein Datentyp für Listen", "Ein Fehlercode"]),
            ("Was ist eine Klasse in Python?", "Ein Codeblock zur Definition von Objekten und deren Verhalten", ["Eine Datenbankstruktur", "Eine Funktion zur Datenanalyse", "Ein spezieller Datentyp"]),
            ("Wie lautet der Standardname für den Konstruktor einer Klasse in Python?", "__init__", ["__constructor__", "__new__", "__class__"]),
            ("Was ist ein Vorteil von Type Hints in Python?", "Bessere Lesbarkeit und Unterstützung durch IDEs", ["Schnellere Ausführung", "Reduzierter Speicherbedarf", "Automatische Fehlerbehebung"]),
            ("Welches Schlüsselwort wird verwendet, um eine Methode in einer Unterklasse zu überschreiben?", "Kein Schlüsselwort erforderlich", ["super", "override", "overwrite"]),
            ("Was ist ein Decorator in Python?", "Eine Funktion, die eine andere Funktion verändert", ["Ein Schlüsselwort zur Definition von Klassen", "Ein Syntaxelement für Variablen", "Eine Datenstruktur"]),
            ("Was ist ein `try-except`-Block in Python?", "Ein Mechanismus zur Behandlung von Ausnahmen", ["Eine Schleife zur Iteration über Fehler", "Ein Dekorator zur Fehlerprotokollierung", "Ein Modul zur Fehlerbehebung"]),
            ("Welche Funktion gibt die Länge einer Liste in Python zurück?", "len()", ["length()", "size()", "count()"]),
            ("Welche der folgenden Aussagen ist korrekt?", "Python unterstützt Mehrfachvererbung", ["Python unterstützt keine Vererbung", "Python benötigt explizite Variablentypen", "Python unterstützt keine Funktionen höherer Ordnung"]),
            ("Wie wird ein Modul in Python importiert?", "import modulename", ["use modulename", "load modulename", "include modulename"])
        ],
        "full-stack": [
            ("Was bedeutet der Begriff 'Full-Stack' in der Webentwicklung?", "Entwicklung des Client- und Server-Teils einer Anwendung", ["Entwicklung von Benutzeroberflächen", "Optimierung von Datenbanken", "Testen von Frontend-Komponenten"]),
            ("Welches Framework wird oft in Python für die Webentwicklung genutzt?", "Flask", ["Django", "React", "Angular"]),
            ("Was ist ein Beispiel für eine Server-Technologie in der Full-Stack Webentwicklung?", "Jinja", ["CSS", "JavaScript", "Bootstrap"]),
            ("Welche Datenbank wird in Flask-Projekten häufig verwendet?", "SQLite", ["PostgreSQL", "MongoDB", "MySQL"]),
            ("Was beschreibt der Begriff 'MVC'?", "Model-View-Controller", ["Main-Version-Control", "Modular-Version-Compilation", "Multi-View-Creation"]),
            ("Was ist eine typische Aufgabe des Controllers im MVC-Muster?", "Benutzereingaben verarbeiten", ["Daten aus der Datenbank anzeigen", "HTML-Seiten stylen", "JSON-Daten speichern"]),
            ("Welche der folgenden Technologien gehört zur Client-Seite einer Webanwendung?", "HTML", ["Flask", "SQLite", "Jinja"]),
            ("Welche Sprache wird genutzt, um die hierarchische Struktur einer Webseite zu definieren?", "HTML", ["CSS", "JavaScript", "Python"]),
            ("Welche Aufgabe hat der View-Teil im MVC-Design?", "Daten visuell darstellen", ["Daten speichern", "Benutzerinteraktionen verarbeiten", "Datenbank-Schemas definieren"]),
            ("Wie nennt man die kleinste lauffähige Version einer Anwendung?", "Minimum Viable Product", ["Minimal Valid Prototype", "Modular Version Program", "Main Validation Process"]),
            ("Was ist der Zweck des Jinja2-Template-Engines?", "Dynamisches Rendern von HTML-Seiten", ["Erstellung und Styling von CSS", "Kompilierung von Python-Skripten", "Verwaltung von JavaScript-Komponenten"]),
            ("Was ist eine typische Aufgabe eines Webservers?", "HTTP-Anfragen verarbeiten und Antworten senden", ["Benutzerinteraktionen analysieren", "Datenbank-Schemas erstellen", "Benutzeroberflächen designen"]),
            ("Welche HTTP-Methode wird verwendet, um Daten auf einem Server zu erstellen?", "POST", ["GET", "PUT", "DELETE"]),
            ("Welcher Begriff beschreibt die Fähigkeit einer Webseite, auf verschiedenen Geräten gut zu funktionieren?", "Responsive Design", ["Skalierbarkeit", "Sicherheit", "Latenzreduzierung"]),
            ("Was ist eine API?", "Eine Schnittstelle für die Interaktion zwischen Softwarekomponenten", ["Eine Programmiersprache", "Ein Webbrowser", "Ein Frontend-Framework"])
        ],
        "github": [
            ("Was ist Git?", "Ein Versionskontrollsystem", ["Eine Datenbank für Softwareprojekte", "Eine Programmiersprache", "Ein Hosting-Dienst für Websites"]),
            ("Was ist GitHub?", "Eine Plattform für die Zusammenarbeit an Projekten mit Git", ["Ein Texteditor", "Ein Tool zur Datenanalyse", "Ein Compiler für Java"]),
            ("Welcher Befehl wird verwendet, um ein Repository zu klonen?", "git clone", ["git fetch", "git pull", "git merge"]),
            ("Was bewirkt der Befehl `git init`?", "Initialisiert ein neues Git-Repository", ["Erstellt eine neue Datei", "Lädt ein bestehendes Repository herunter", "Startet den Git-Server"]),
            ("Was ist ein 'Commit' in Git?", "Ein Schnappschuss des aktuellen Projektzustands", ["Eine neue Datei", "Eine Fehlermeldung", "Eine Verzweigung im Projekt"]),
            ("Welche Datei sollte genutzt werden, um bestimmte Dateien oder Verzeichnisse vom Git-Tracking auszuschließen?", ".gitignore", [".exclude", ".gitconfig", ".trackignore"]),
            ("Was bewirkt der Befehl `git status`?", "Zeigt den Zustand des Arbeitsverzeichnisses und der Staging-Area", ["Zeigt den aktuellen Branch an", "Zeigt die Liste aller Commits", "Erstellt einen neuen Branch"]),
            ("Welcher Befehl wird verwendet, um Änderungen zu einer neuen Version hinzuzufügen?", "git add", ["git commit", "git merge", "git branch"]),
            ("Was passiert bei einem `git merge`?", "Zwei Branches werden zusammengeführt", ["Eine Datei wird gelöscht", "Ein Repository wird initialisiert", "Änderungen werden zurückgesetzt"]),
            ("Welche Datei enthält Metadaten über ein Git-Repository?", ".git", [".gitconfig", ".metadata", ".gitignore"]),
            ("Was ist ein Branch in Git?", "Eine parallele Entwicklungslinie", ["Ein Backup des Projekts", "Eine entfernte Kopie des Repositories", "Ein einzelnes Commit"]),
            ("Was ist ein Pull Request auf GitHub?", "Eine Anfrage, Änderungen in einen Branch zu integrieren", ["Eine Anfrage, ein Repository zu klonen", "Eine Anfrage, ein Repository zu löschen", "Eine Anfrage, einen Commit rückgängig zu machen"]),
            ("Welcher Befehl wird verwendet, um Änderungen von einem Remote-Repository zu holen?", "git fetch", ["git clone", "git merge", "git push"]),
            ("Welche Funktion hat GitHub Pages?", "Erstellung statischer Websites aus Markdown-Dateien", ["Hosting von Datenbanken", "Kompilierung von Python-Skripten", "Automatische Projekt-Dokumentation"]),
            ("Was ist der Zweck von `git log`?", "Zeigt die Versionsgeschichte des Repositories", ["Erstellt ein neues Repository", "Zeigt die Liste der ignorierten Dateien", "Löscht alte Commits"])
        ],
        "flask": [
            ("Was ist Flask?", "Ein Python-Webframework", ["Eine Datenbank", "Ein CSS-Framework", "Ein JavaScript-Tool"]),
            ("Welches Design-Muster unterstützt Flask?", "Model-View-Controller (MVC)", ["Singleton", "Observer", "Factory"]),
            ("Wie definiert man eine Route in Flask?", "@app.route()", ["app.url()", "route.define()", "app.connect()"]),
            ("Welche Methode wird genutzt, um Daten an den Server zu senden?", "POST", ["GET", "DELETE", "PATCH"]),
            ("Welche Template-Engine verwendet Flask?", "Jinja2", ["Handlebars", "Mustache", "EJS"]),
            ("Was bewirkt `app.run()` in Flask?", "Startet den Webserver", ["Erstellt eine Datenbank", "Initialisiert die Anwendung", "Kompiliert den Code"]),
            ("Welche HTTP-Methode wird genutzt, um Daten von einem Server abzurufen?", "GET", ["POST", "PUT", "DELETE"]),
            ("Was ist der Standardport für Flask-Anwendungen?", "5000", ["8080", "80", "3000"]),
            ("Wie können Variablen an ein HTML-Template übergeben werden?", "Mit `render_template()`", ["Mit `template_load()`", "Mit `send_data()`", "Mit `pass_variable()`"]),
            ("Wie können Fehlerseiten (z. B. 404) in Flask behandelt werden?", "Mit der Methode `@app.errorhandler()`", ["Mit einer Datenbankabfrage", "Durch Erstellen eines zusätzlichen HTML-Files", "Mit einer Middleware"]),
            ("Welches Modul wird für den Zugriff auf HTTP-Requests in Flask verwendet?", "request", ["http", "flask_http", "api"]),
            ("Wie definiert man eine API-Route in Flask, die JSON zurückgibt?", "Mit `@app.route()` und `return jsonify()`", ["Mit `@api.route()`", "Mit `@json.route()`", "Mit `@app.json()`"]),
            ("Welche Flask-Erweiterung wird häufig für Formulare verwendet?", "Flask-WTF", ["Flask-SQLAlchemy", "Flask-CSS", "Flask-Forms"]),
            ("Was ist der Zweck des `debug`-Modus in Flask?", "Fehler während der Entwicklung besser sichtbar zu machen", ["Die Anwendung schneller zu machen", "Den Code zu kompilieren", "Datenbankverbindungen zu optimieren"]),
            ("Welche Datenbank wird oft mit Flask für kleine Projekte verwendet?", "SQLite", ["PostgreSQL", "MongoDB", "MySQL"])
        ],
        "designentscheidungen": [
            ("Was ist eine Designentscheidung im Kontext der Softwareentwicklung?", "Eine Lösung für ein nicht triviales Problem", ["Die Auswahl einer Programmiersprache", "Die Erstellung von Benutzerdokumentationen", "Das Testen eines Moduls"]),
            ("Was beschreibt ein Designentscheidungsdokument?", "Den Grund für eine bestimmte technische Wahl", ["Den Code einer Anwendung", "Den Marktwert eines Produkts", "Die Anzahl der Benutzer"]),
            ("Welches Ziel haben dokumentierte Designentscheidungen?", "Entscheidungen nachvollziehbar zu machen", ["Die Codequalität zu verbessern", "Fehler zu minimieren", "Softwaretests zu vereinfachen"]),
            ("Welche der folgenden Phasen gehört zur Dokumentation von Designentscheidungen?", "Analysieren", ["Codieren", "Implementieren", "Debuggen"]),
            ("Was gehört **nicht** zu den 5Cs der dokumentierten Designentscheidungen?", "Compile", ["Create", "Communicate", "Coach"]),
            ("Wie können Designentscheidungen neuen Teammitgliedern helfen?", "Durch Onboarding und Einarbeitung", ["Durch Code-Optimierung", "Durch schnellere Projektabschlüsse", "Durch automatische Fehlerbehebung"]),
            ("Welches Element gehört typischerweise zu einem Designentscheidungsdokument?", "Begründung der getroffenen Entscheidung", ["UML-Diagramme", "Marketingpläne", "Endnutzerberichte"]),
            ("Warum ist es wichtig, Designentscheidungen zu dokumentieren?", "Um zukünftige Änderungen zu erleichtern", ["Um Kosten zu senken", "Um Code zu minimieren", "Um Benutzeroberflächen zu gestalten"]),
            ("Was beschreibt die Phase 'Priorisieren' bei Designentscheidungen?", "Die Bewertung, welche Entscheidungen zuerst getroffen werden sollten", ["Die Implementierung des Designs", "Die Erstellung von Prototypen", "Die Planung von Tests"]),
            ("Was unterscheidet Designentscheidungen von UML-Diagrammen?", "Designentscheidungen erklären das 'Warum' hinter einer Wahl", ["UML-Diagramme sind weniger visuell", "UML-Diagramme enthalten keine technische Details", "Designentscheidungen beinhalten Code-Snippets"]),
            ("Welche der folgenden Aussagen beschreibt die Phase 'Analysieren' korrekt?", "Technische Optionen werden bewertet", ["Das Projekt wird abgeschlossen", "Tests werden durchgeführt", "Die Benutzeroberfläche wird gestaltet"]),
            ("Wie können Designentscheidungen bei Änderungen der Anforderungen nützlich sein?", "Sie helfen, die ursprünglichen Annahmen zu verstehen", ["Sie eliminieren unnötigen Code", "Sie automatisieren den Prozess", "Sie reduzieren Entwicklungszeit"]),
            ("Welche Technologie wird empfohlen, um Designentscheidungen in Markdown zu dokumentieren?", "GitHub Pages", ["Microsoft Word", "PowerPoint", "Excel"]),
            ("Welche Phase folgt nach der Dokumentation einer Designentscheidung?", "Implementierung", ["Testen", "Validierung", "Analyse"]),
            ("Wie kann man dokumentierte Designentscheidungen effizient verwalten?", "Mit einem Versionskontrollsystem wie Git", ["Durch Speichern in einer Datenbank", "Mit einer Textverarbeitungssoftware", "Durch regelmäßige Meetings"])
        ],
        "frontend": [
            ("Wofür steht HTML?", "Hypertext Markup Language", ["Hypertext Modeling Language", "Hyperlink Text Management", "Hyperlink Markup List"]),
            ("Wofür steht CSS?", "Cascading Style Sheets", ["Cascading Style System", "Cascading Sheet Styles", "Computer Style Syntax"]),
            ("Welche Aufgabe hat HTML in der Webentwicklung?", "Struktur und Inhalt von Webseiten definieren", ["Webseiten dynamisch machen", "Benutzerinteraktionen verarbeiten", "Daten speichern"]),
            ("Welche Aufgabe hat CSS in der Webentwicklung?", "Die visuelle Gestaltung von Webseiten steuern", ["Datenbanken verbinden", "HTTP-Anfragen senden", "Daten auf der Konsole ausgeben"]),
            ("Welche der folgenden Technologien wird NICHT als Frontend-Technologie betrachtet?", "Flask", ["HTML", "CSS", "JavaScript"]),
            ("Welche Eigenschaft wird verwendet, um die Farbe von Text in CSS zu ändern?", "color", ["background-color", "font-color", "text-color"]),
            ("Welche CSS-Eigenschaft wird verwendet, um den Text zu zentrieren?", "text-align", ["align-items", "justify-content", "center"]),
            ("Wie definiert man einen Link in HTML?", "<a href=\"url\">Link</a>", ["<link href=\"url\">", "<url>Link</url>", "<href>Link</href>"]),
            ("Was ist ein Inline-Element in HTML?", "Ein Element, das keinen eigenen Block erstellt", ["Ein Element, das auf einer eigenen Zeile steht", "Ein Element, das nur mit CSS gestylt werden kann", "Ein Element, das immer interaktiv ist"]),
            ("Welche Eigenschaft wird verwendet, um Abstände außerhalb eines Elements zu definieren?", "margin", ["padding", "border", "spacing"]),
            ("Was macht die CSS-Eigenschaft `display: none`?", "Sie versteckt ein Element und entfernt es aus dem Layoutfluss", ["Sie entfernt die Hintergrundfarbe eines Elements", "Sie zeigt ein Element in kleiner Größe an", "Sie ändert die Transparenz eines Elements"]),
            ("Was ist der Unterschied zwischen `id` und `class` in HTML?", "`id` ist eindeutig, `class` kann mehrfach verwendet werden", ["`id` kann mehrfach verwendet werden, `class` nicht", "`class` ist für JavaScript, `id` nur für CSS", "Es gibt keinen Unterschied"]),
            ("Welche CSS-Eigenschaft wird genutzt, um die Schriftgröße zu ändern?", "font-size", ["text-size", "size", "font-weight"]),
            ("Welches HTML-Element wird für Tabellen verwendet?", "<table>", ["<grid>", "<layout>", "<div>"]),
            ("Was bedeutet „Responsive Design“?", "Webseiten, die auf verschiedenen Geräten gut aussehen", ["Webseiten, die schnell laden", "Webseiten mit einfacher Navigation", "Webseiten mit dynamischen Inhalten"])
        ],
        "benutzeroberflächen": [
            ("Was ist WTForms?", "Eine Python-Bibliothek für die Validierung von Formularen", ["Ein CSS-Framework für Styling", "Ein Tool zur Datenbankverwaltung", "Ein JavaScript-Framework"]),
            ("Wofür wird Bootstrap verwendet?", "Zur Gestaltung und Strukturierung von Benutzeroberflächen", ["Zur Erstellung von APIs", "Zum Entwickeln von Datenbanken", "Zum Schreiben von Backend-Logik"]),
            ("Was ermöglicht Flask-WTF?", "Eine einfache Integration von WTForms in Flask", ["Die Erstellung von Datenbanken", "Die Generierung von CSS-Dateien", "Die Optimierung von Flask-Routen"]),
            ("Welche Sprache nutzt Bootstrap hauptsächlich?", "CSS", ["Python", "Java", "Ruby"]),
            ("Welche Komponente wird in Bootstrap für Navigationselemente verwendet?", "nav", ["menu", "header", "navigator"]),
            ("Welche Methode bietet WTForms zur Validierung von Formulardaten?", "validate_on_submit()", ["check_data()", "form_validator()", "is_valid()"]),
            ("Welche CSS-Klasse wird in Bootstrap für einen Button mit der Farbe Blau verwendet?", "btn-primary", ["btn-red", "btn-info", "btn-success"]),
            ("Welche Funktion erfüllt die Flask-WTF-Erweiterung?", "Generiert HTML-Formulare mit Python", ["Erstellt Bootstrap-Komponenten", "Optimiert die Datenbankleistung", "Bietet Funktionen für Benutzerregistrierung"]),
            ("Wie wird in WTForms ein Textfeld erstellt?", "StringField()", ["TextArea()", "TextField()", "InputField()"]),
            ("Was ist ein Vorteil von Bootstrap?", "Es bietet vorgefertigte, responsive CSS-Komponenten", ["Es reduziert die Ladezeit einer Webseite", "Es unterstützt nur statische Webseiten", "Es erstellt automatisch Datenbanken"]),
            ("Welche Bootstrap-Klasse wird verwendet, um ein Layout in Spalten zu teilen?", "col", ["row", "grid", "table"]),
            ("Welche WTForms-Funktion wird verwendet, um Formulardaten zu speichern?", "populate_obj()", ["save_form()", "store_data()", "serialize()"]),
            ("Wie wird Bootstrap in eine HTML-Datei eingebunden?", "Mit einem <link>-Tag, das auf eine CDN-URL verweist", ["Mit einem Python-Skript", "Durch manuelles Schreiben von CSS", "Durch Installation über Flask"]),
            ("Welche Bootstrap-Klasse wird verwendet, um ein Formular horizontal auszurichten?", "form-inline", ["form-group", "form-horizontal", "form-stacked"]),
            ("Welche Bootstrap-Komponente wird verwendet, um modale Fenster zu erstellen?", "modal", ["window", "popup", "alert"])
        ],
    }

    def create_quiz(category, question_data):
        return Quiz(
            category=category,
            question=question_data[0],
            correct_answer=question_data[1],
            wrong_answer1=question_data[2][0],
            wrong_answer2=question_data[2][1],
            wrong_answer3=question_data[2][2]
        )

    with app.app_context():
        try:
            db.session.query(Quiz).delete()
            questions = [
                create_quiz(cat, q) 
                for cat, q_list in questions_data.items() 
                for q in q_list
            ]
            db.session.bulk_save_objects(questions)
            db.session.commit()
            
            logger.info(f'Added {len(questions)} new questions')
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error adding questions: {str(e)}')
            return False

if __name__ == "__main__":
    add_sample_questions()