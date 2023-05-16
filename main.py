from website import create_app

app = create_app()

'''
Tylko jezeli uruchomie ten plik to web serwer sie odpali. Import nie zadziala.
debug=True restartuje serwer za kazdym razem gdy bedzie zmiana w kodzie.
'''
if __name__ == '__main__':
    app.run(debug=True)
