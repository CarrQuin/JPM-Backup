# # Leitfaden für die Website-Wartung

## Kapitel 1: Einleitung

Dieses Dokument soll den Benutzern eine detaillierte Anleitung bieten, um die Website effizienter zu warten und zu optimieren. Die Hauptthemen umfassen:

1. **Wartung benutzerdefinierter Hooks und Filter in den Theme-Dateien sowie Custom CSS**: Anpassung durch manuelle Codierung, um spezifische Anforderungen zu erfüllen, Plugin-Konflikte zu vermeiden und die Seiteninhalte sowie das Design einheitlich zu gestalten.  
2. **Verwendung des Simple Membership-Plugins**: Anleitung zu häufigen Vorgängen und wichtigen Aspekten bei der Verwaltung von Abonnement-Systemen, um eine reibungslose Nutzung der Mitgliederfunktionen zu gewährleisten.  
3. **Power BI-Datenintegration**: Erläuterung, wie Power BI-Daten in die Website eingebettet werden können, einschließlich der Nutzung von Simple Membership zur Steuerung der Inhaltszugänglichkeit.  

---

## Kapitel 2: Benutzerdefinierte Inhalte in WordPress

### 2.1.1 Benutzerdefinierte Funktionen in den Theme-Dateien

Obwohl WordPress eine benutzerfreundliche Oberfläche und zahlreiche Plugins bietet, basiert es auf einem PHP-Framework. Bei komplexen Anforderungen oder Plugin-Konflikten ist oft die manuelle Erstellung von Hooks und Filtern erforderlich. Dies setzt Grundkenntnisse in PHP und CSS voraus.   

> **Hinweis**: Da benutzerdefinierte Inhalte bei WordPress- oder Plugin-Updates überschrieben werden können, ist eine regelmäßige Back-up des Website-Quellcodes entscheidend.

Für das auf dieser Website genutzte OceanWP-Theme unterscheidet sich die Dateistruktur von klassischen WordPress-Themes. Die folgenden Schritte beschreiben die Vorgehensweise:  

1. Navigieren Sie im linken Menü zu **Design > Theme-Datei-Editor**.  
2. Stellen Sie sicher, dass das aktuell aktive Theme ausgewählt ist.  
3. Wählen Sie in der Dateiliste rechts die Datei `Theme-Funktionen` (entspricht `functions.php`) aus.  
4. Benutzerdefinierte Funktionen befinden sich meist am Anfang der Datei und sind durch doppelte Kommentarzeichen von den Theme-eigenen Inhalten abgegrenzt.  

Ein Beispiel ist eine Funktion namens `login_logout_menu_`, die speziell für die Steuerung der Logik von Menüoptionen in der oberen Navigationsleiste entwickelt wurde und mit dem Plugin „Login Logout Menu“ kompatibel ist.  

---

### 2.1.2 Wichtige Hinweise beim Bearbeiten von Theme-Dateien

Beim Bearbeiten der Datei `functions.php` sind folgende Punkte zu beachten:  

1. **Einschränkungen bei der Erstellung von Child-Themes**  
   Da die aktuelle Umgebung keinen direkten Zugriff auf die Website-Dateien erlaubt, können benutzerdefinierte Inhalte nicht durch die Erstellung eines Child-Themes gesichert werden. Benutzerdefinierter Code kann daher bei Theme-Updates verloren gehen.  

2. **Einfluss von Domain-Änderungen**  
   Vermeiden Sie die Verwendung von `site_url( '/Website/' )` in Links, da dies bei Domain-Änderungen zu Fehlern führen kann. Stattdessen wird `home_url( '/Website/' )` empfohlen.  

3. **Logikkonflikte zwischen Plugins**  
   Alle Filter, die mit dem Plugin „Login Logout Menu“ zusammenhängen, können die Logik von URLs für Login, Registrierung, Benutzerinformationen und Logout beeinflussen.  

4. **Konflikte mit Simple Membership-Einstellungen**  
   Überprüfen Sie vor der Änderung von Links die Weiterleitungseinstellungen im Simple Membership-Plugin, um Konflikte mit den Weiterleitungslogiken des Plugins „Login Logout Menu“ zu vermeiden.  

5. **Problem mit Standard-Login-Links**  
   Das Plugin „Login Logout Menu“ setzt den Standard-Login-Link auf `/wp-admin`, was die Funktionalität von Sicherheits-Plugins wie „WPS Hide Login“ beeinträchtigen kann. Stellen Sie sicher, dass der Login-Link auf die korrekte Benutzeranmeldeseite verweist.  
