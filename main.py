from collections import Counter

class CriptoanalisisVigenere:
    def __init__(self):
        self.ALFABETO = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

        self.LONGITUD_ALFABETO = len(self.ALFABETO)
        # https://es.sttmedia.com/frecuencias-de-letras-ingles
        self.FRECUENCIAS = {
            'A': 8.34, 'B': 1.54, 'C': 2.73, 'D': 4.14, 'E': 12.6, 'F': 2.03,
            'G': 1.92, 'H': 6.11, 'I': 6.71, 'J': 0.23, 'K': 0.87, 'L': 4.24,
            'M': 2.53, 'N': 6.80, 'O': 7.7, 'P': 1.66, 'Q': 0.09, 'R': 5.68,
            'S': 6.11, 'T': 9.37, 'U': 2.85, 'V': 1.06, 'W': 2.34, 'X': 0.20,
            'Y': 2.04, 'Z': 0.06
        }

    def formateoDeTexto(self, texto: str) -> str:
        """Limpia el texto de entrada, convirtiéndolo a mayúsculas y filtrando solo caracteres del alfabeto español."""
        texto_formateado = ""
        for letra in texto.upper():
            if letra == 'Ñ':
                texto_formateado += 'GN'
            elif letra in self.ALFABETO:
                texto_formateado += letra
        return texto_formateado 

    def vigenere(self, mensaje: str, clave: str, cifrado: bool) -> str:
        clave_formateada = self.formateoDeTexto(clave)
        if not clave_formateada:
            return mensaje

        longitudClave = len(clave_formateada)
        resultado = ""
        
        for i in range(len(mensaje)):
            letraMensaje = mensaje[i]
            letraClave = clave_formateada[i % longitudClave]   
            
            valorLetraMensaje = self.ALFABETO.index(letraMensaje)
            valorLetraClave = self.ALFABETO.index(letraClave)
            
            if cifrado:
                valorCifrado = (valorLetraMensaje + valorLetraClave) % self.LONGITUD_ALFABETO  
                letraCifrada = self.ALFABETO[valorCifrado]
                resultado+=(letraCifrada)
            else:
                valorDescifrado = (valorLetraMensaje - valorLetraClave) % self.LONGITUD_ALFABETO  
                letraDescifrada = self.ALFABETO[valorDescifrado]  
                resultado+=(letraDescifrada)

        return resultado
    
    def calcularIndiceDeCoincidencias(self, texto):
        counts = Counter(texto)
        tamanioTexto = len(texto) 
        
        if tamanioTexto <= 1: return 0 

        numerator = sum(n * (n - 1) for n in counts.values())
        denominator = tamanioTexto * (tamanioTexto - 1)

        return numerator / denominator

    def calcularChiCuadrado(self, text):
        N = len(text)
        if N == 0:
            return 0.0
        
        conteoGeneral = Counter(text)
        valorChiCuadrado = 0.0

        for letra, frecuenciaEsperada in self.FRECUENCIAS.items():
            conteoParticular = conteoGeneral.get(letra, 0)
            conteoEsperado = N * (frecuenciaEsperada / 100)

            if conteoEsperado == 0:
                continue

            valorChiCuadrado += ((conteoParticular - conteoEsperado) ** 2) / conteoEsperado

        return valorChiCuadrado

    def longitudClave(self, textoCifrado: str, maximaLongitud: int = 20) -> int:
        mejorIC = 0.0
        mejorLongitud = 0
        
        print("Estimando longitud de clave")
        for longitud in range(1, maximaLongitud + 1):
            columnas = [""] * longitud
            for i, caracter in enumerate(textoCifrado):
                columnas[i % longitud] += caracter
            
            icPromedio = sum(self.calcularIndiceDeCoincidencias(col) for col in columnas) / longitud
            print(f"Longitud {longitud:2}: IC promedio = {icPromedio:.4f}")
            if icPromedio > mejorIC:
                mejorIC = icPromedio
                mejorLongitud = longitud
                
        print(f"\nLongitud más probable: {mejorLongitud} (IC = {mejorIC:.4f})")
        return mejorLongitud

    def encontrarClave(self, textoCifrado: str, longitudClave: int) -> str:
        columnas = [""] * longitudClave
        for i, caracter in enumerate(textoCifrado):
            columnas[i % longitudClave] += caracter
            
        clave = ""

        print("Estimando Clave")
        for i, col in enumerate(columnas):
            mejorChi = float('inf')
            mejorLetra = ''
            for indice in range(self.LONGITUD_ALFABETO):
                letraIndice = self.ALFABETO[indice]
                colDescifrada = self.vigenere(col, letraIndice, cifrado = False)
                valorChi = self.calcularChiCuadrado(colDescifrada) 
                
                if valorChi < mejorChi:
                    mejorChi = valorChi
                    mejorLetra = letraIndice
            clave += mejorLetra
            print(f"Columna {i+1:2}/{longitudClave}: Letra de clave encontrada = '{mejorLetra}'")

        print(f"\nClave encontrada: {clave}\n")
        return clave

# --- VARIABLES DE PRUEBA ---
TEXTOAROMPER = """UECWKDVLOTTVACKTPVGEZQMDAMRNPDDUXLBUICAMRHOECBHSPQLVIWO
FFEAILPNTESMLDRUURIFAEQTTPXADWIAWLACCRPBHSRZIVQWOFROGTT
NNXEVIVIBPDTTGAHVIACLAYKGJIEQHGECMESNNOCTHSGGNVWTQHKBPR
HMVUOYWLIAFIRIGDBOEBQLIGWARQHNLOISQKEPEIDVXXNETPAXNZGDX
WWEYQCTIGONNGJVHSQGEATHSYGSDVVOAQCXLHSPQMDMETRTMDUXTEQQ
JMFAEEAAIMEZREGIMUECICBXRVQRSMENNWTXTNSRNBPZHMRVRDYNECG
SPMEAVTENXKEQKCTTHSPCMQQHSQGTXMFPBGLWQZRBOEIZHQHGRTOBSG
TATTZRNFOSMLEDWESIWDRNAPBFOFHEGIXLFVOGUZLNUSRCRAZGZRTTA
YFEHKHMCQNTZLENPUCKBAYCICUBNRPCXIWEYCSIMFPRUTPLXSYCBGCC
UYCQJMWIEKGTUBRHVATTLEKVACBXQHGPDZEANNTJZTDRNSDTFEVPDXK
TMVNAIQMUQNOHKKOAQMTBKOFSUTUXPRTMXBXNPCLRCEAEOIAWGGVVUS
GIOEWLIQFOZKSPVMEBLOHLXDVCYSMGOPJEFCXMRUIGDXNCCRPMLCEWT
PZMOQQSAWLPHPTDAWEYJOGQSOAVERCTNQQEAVTUGKLJAXMRTGTIEAFW
PTZYIPKESMEAFCGJILSBPLDABNFVRJUXNGQSWIUIGWAAMLDRNNPDXGN
PTTGLUHUOBMXSPQNDKBDBTEECLECGRDPTYBVRDATQHKQJMKEFROCLXN
FKNSCWANNAHXTRGKCJTTRRUEMQZEAEIPAWEYPAJBBLHUEHMVUNFRPVM
EDWEKMHRREOGZBDBROGCGANIUYIBNZQVXTGORUUCUTNBOEIZHEFWNBI
GOZGTGWXNRHERBHPHGSIWXNPQMJVBCNEIDVVOAGLPONAPWYPXKEFKOC
MQTRTIDZBNQKCPLTTNOBXMGLNRRDNNNQKDPLTLNSUTAXMNPTXMGEZKA
EIKAGQ"""

TEXTO_EJEMPLO_CLARO = "Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona.Este es un mensaje de prueba para el cifrado Vigenere, mañana veremos si funciona."

def main():
    analizador = CriptoanalisisVigenere()

    print("--- EJEMPLO DE CIFRADO/DESCIFRADO ---")
    clave_ejemplo = "SECRETO"
    
    texto_ejemplo_limpio = analizador.formateoDeTexto(TEXTO_EJEMPLO_CLARO)
    
    print(f"\nTexto original formateado: {''.join(texto_ejemplo_limpio)}")
    print(f"\nClave: {clave_ejemplo}")

    texto_cifrado_ejemplo = analizador.vigenere(texto_ejemplo_limpio, clave_ejemplo, cifrado=True)
    print(f"\nTexto cifrado: {''.join(texto_cifrado_ejemplo)}")

    texto_descifrado_ejemplo = analizador.vigenere(texto_cifrado_ejemplo, clave_ejemplo, cifrado=False)
    print(f"\nTexto descifrado: {''.join(texto_descifrado_ejemplo)}\n")

    print("\n--- ANÁLISIS DE TEXTOAROMPER ---")
    
    textoLimpioARomper = analizador.formateoDeTexto(TEXTOAROMPER)
    longitud = analizador.longitudClave(textoLimpioARomper)
    clave = analizador.encontrarClave(textoLimpioARomper, longitud)
    texto = analizador.vigenere(textoLimpioARomper, clave, cifrado=False)
    
    print("Texto final descifrado de TEXTOAROMPER:")
    for letra in texto:
        print(letra, end="")
    print("\n")

if __name__ == "__main__":
    main()