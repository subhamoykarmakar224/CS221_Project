from app.app import webapp

# Start Web App
if __name__ == '__main__':
    webapp.run(debug=True)


# TODO :: Delete below later
# from app.GetData import GetData
# from datetime import datetime

# if __name__ == '__main__':
#     g = GetData()
#     t1 = datetime.now()
#     print(g.get_data('levorato'))
#     t2 = datetime.now()

#     print(f'Exec Time {t2 - t1}')
