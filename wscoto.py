import requests
from bs4 import BeautifulSoup

def buscarProductosCoto():
    limite = 0
    lenAnterior = 0
    productosArray = buscarProductosCotoDesde(limite)
    while (lenAnterior < len(productosArray)):
        limite = limite + 1000
        lenAnterior = len(productosArray)
        productosArray = productosArray + buscarProductosCotoDesde(limite)
    return productosArray


def buscarProductosCotoDesde(desde):
    url=('https://www.cotodigital3.com.ar/sitios/cdigi/browse?No='+str(desde)+'&Nrpp=1000')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    productos = soup.find_all('li', class_=["clearfix"])

    productosArray = []
    for producto in productos:
        productoDict = {}
        pro = producto.find(class_="descrip_full")
        if pro is not None:
            pro=pro.get_text().replace("\n", " ").strip()
        pre = producto.find(class_="atg_store_newPrice")
        if pre is not None:
            pre=pre.get_text().replace("\n", " ").replace("PRECIO CONTADO","").strip()
        productoDict['producto'] = pro
        productoDict['precio'] = pre
        productosArray.append(productoDict)
    return productosArray


if __name__ == '__main__':

    ivicecs=buscarProductosCoto()
    print(len(ivicecs))
    f = open("ivicec.txt", "a")
    for ivice in ivicecs:
        f.write(ivice['producto']+';'+ivice['precio']+'\n')
    f.close()
