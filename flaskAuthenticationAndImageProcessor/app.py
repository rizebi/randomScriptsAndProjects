import image_processor

if __name__ == '__main__':

    app = image_processor.create_app()
    app.run(debug=True, host='0.0.0.0', port=80)
