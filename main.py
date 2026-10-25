import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label='Tipo', width=300)
    input_marca = ft.TextField(label='Marca', width=300)
    input_anno = ft.TextField(label='Anno acquisto', width=300)
    valore_contatore = ft.TextField(value='0', width=60, text_align=ft.TextAlign.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def decrementa_valore(e):
        try:
            valore = float(valore_contatore.value)
            if valore >= 10:
                valore_contatore.value = str(int(valore-10))
            else:
                valore_contatore.value = "0"
        except ValueError:
            valore_contatore.value = "10"

    def incrementa_valore(e):
        try:
            valore = float(valore_contatore.value)
            valore_contatore.value = str(int(valore+10))
        except ValueError:
            valore_contatore.value = "10"

    def aggiungi_strumento(e):
        tipo = input_tipo.value
        marca = input_marca.value
        str_anno = input_anno.value
        str_valore = valore_contatore.value
        if not tipo or not marca or not str_anno:
            alert.show_alert("Errore: Compilare tutti i campi per inserire lo strumento.")
            return
        try:
            anno = int(str_anno)
        except ValueError:
            alert.show_alert("Errore: Il campo Anno acquisto deve essere un intero valido.")
            return
        try:
            valore = float(str_valore)
            if valore < 0:
                alert.show_alert("Errore: il valore dello strumento non può essere negativo.")
                return
        except:
            alert.show_alert("Errore: Il valore dello strumento deve essere un numero valido.")
            return
        deposito.aggiungi_strumento(tipo, marca, anno, valore)
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        valore_contatore.value = "0"
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_meno = ft.IconButton(ft.Icons.REMOVE, icon_color='red', on_click=decrementa_valore)
    pulsante_piu = ft.IconButton(ft.Icons.ADD, icon_color='green', on_click=incrementa_valore)
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(spacing=50,
               controls=[input_tipo, input_marca, input_anno, pulsante_meno, valore_contatore, pulsante_piu],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
