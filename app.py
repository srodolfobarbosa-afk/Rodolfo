from app import create_app, socketio

app = create_app()

# A linha abaixo é para desenvolvimento local e não deve ser usada em produção com Gunicorn.
# if __name__ == "__main__":
#    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

# Para deploy com Gunicorn, o Gunicorn irá importar e executar a instância 'app' diretamente.


