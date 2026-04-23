import random
import os
import sys
import csv
import math
from datetime import datetime
from typing import Callable, Any, Union, List, Set, Dict
from collections import Counter

# ═══════════════════════════════════════════════════════════
# SECCIÓN 2: CONFIGURACIÓN DE INTERFAZ (Colores, Headers, Tablas)
# ═══════════════════════════════════════════════════════════

COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"

def setup_environment():
    """Configura el entorno para el ejecutable portable y la consola Windows.

    Asegura que el título de la ventana esté configurado y que la carpeta de resultados exista.
    """
    os.system('')
    os.system("title Stat-Sim Pro - Motor de Probabilidad")
    ensure_results_folder()

def get_base_path() -> str:
    """Detecta la ruta raíz del programa, ya sea como script o como .exe compilado.

    Returns:
        str: Ruta absoluta al directorio base.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def ensure_results_folder() -> str:
    """Crea la carpeta de resultados relativa a la ubicación del ejecutable.

    Returns:
        str: Ruta de la carpeta de resultados.
    """
    base_path = get_base_path()
    folder_path = os.path.join(base_path, "Resultados_Simulacion")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def clear_screen():
    """Limpia la pantalla de la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_ui_header(titulo: str, modulo: str = None):
    """Limpia la pantalla y dibuja el encabezado con sistema de migas de pan.

    Args:
        titulo (str): Texto del título principal.
        modulo (str, optional): Nombre del módulo para el breadcrumb.
    """
    clear_screen()
    breadcrumb = f"ESTADÍSTICA PRO > {modulo if modulo else 'PRINCIPAL'}"
    print(f"{COLOR_CYAN}{COLOR_BOLD}{breadcrumb}{COLOR_RESET}")
    print(f"{COLOR_CYAN}━" * 60 + f"{COLOR_RESET}")
    print(f"\n{COLOR_BOLD}{titulo}{COLOR_RESET}\n")

def draw_table(headers: List[str], rows: List[List[Any]]):
    """Dibuja una tabla profesional con bordes usando caracteres de dibujo.

    Args:
        headers (List[str]): Lista de encabezados de columna.
        rows (List[List[Any]]): Datos organizados en filas.
    """
    if not rows:
        print(f"{COLOR_RED}No hay datos disponibles para mostrar en tabla.{COLOR_RESET}")
        return

    col_widths = []
    for i, header in enumerate(headers):
        max_w = len(header)
        for row in rows:
            if i < len(row):
                max_w = max(max_w, len(str(row[i])))
        col_widths.append(max_w)

    top = "┌" + "─" * (col_widths[0] + 2)
    for w in col_widths[1:]:
        top += "┬" + "─" * (w + 2)
    top += "┐"

    head_str = "│"
    for i, h in enumerate(headers):
        head_str += f" {h:<{col_widths[i]}} " + "│"

    div = "├" + "─" * (col_widths[0] + 2)
    for w in col_widths[1:]:
        div += "┼" + "─" * (w + 2)
    div += "┤"

    row_strs = []
    for row in rows:
        r_str = "│"
        for i, val in enumerate(row):
            r_str += f" {str(val):<{col_widths[i]}} " + "│"
        row_strs.append(r_str)

    bot = "└" + "─" * (col_widths[0] + 2)
    for w in col_widths[1:]:
        bot += "┴" + "─" * (w + 2)
    bot += "┘"

    print(top)
    print(head_str)
    print(div)
    for rs in row_strs:
        print(rs)
    print(bot)

def print_banner():
    """Muestra el banner ASCII de STAT-SIM PRO v1.0."""
    banner = f"""
{COLOR_CYAN}
  ███████╗ ████████╗   ██████╗     ██████╗ ██████╗
  ██╔════╝ ╚══██╔══╝   ██╔═══██╗   ██╔══██╗██╔══██╗
  ███████╗    ██║      ██║   ██║   ██████╔╝██████╔╝
  ╚════██║    ██║      ██║   ██║   ██╔═══╝ ██╔═══╝
  ███████║    ██║      ██║   ██║   ██║     ██║
  ╚══════╝    ╚═╝      ╚═╝   ╚═╝   ╚═╝     ╚═╝
                             v1.0 EDITION
{COLOR_RESET}
    """
    print(banner)

# ═══════════════════════════════════════════════════════════
# SECCIÓN 4: FUNCIONES DE ENTRADA VALIDADAS
# ═══════════════════════════════════════════════════════════

def safe_input(prompt: str, default: str = "") -> str:
    """Maneja entradas del usuario evitando colapsos por KeyboardInterrupt o EOFError."""
    try:
        user_input = input(f"{COLOR_CYAN}{prompt}{COLOR_RESET}")
        return user_input.strip() if user_input.strip() != "" else default
    except (KeyboardInterrupt, EOFError):
        print(f"\n{COLOR_YELLOW}Operación cancelada por el usuario.{COLOR_RESET}")
        return default

def get_valid_int(prompt: str, min_val: int = 1) -> int:
    """Validador genérico de enteros."""
    while True:
        try:
            user_input = input(f"{COLOR_CYAN}{prompt}{COLOR_RESET}")
            if user_input.strip() == "": return min_val
            n = int(user_input)
            if n < min_val:
                print(f"{COLOR_RED}Error: Ingrese un número mayor o igual a {min_val}.{COLOR_RESET}")
                continue
            return n
        except ValueError:
            print(f"{COLOR_RED}Error: Entrada no válida. Debe ingresar un número entero.{COLOR_RESET}")

def didactic_prompt(prompt: str, example: str) -> str:
    """Formatea un prompt de entrada con instrucciones didácticas."""
    formatted = f"({COLOR_YELLOW}{COLOR_BOLD}?{COLOR_RESET}) {prompt}. {COLOR_YELLOW}Ejemplo: {example}{COLOR_RESET}"
    return safe_input(formatted)

def get_didactic_int(prompt: str, example: str, min_val: int = 1) -> int:
    """Wrapper de get_valid_int con formato didáctico."""
    formatted_prompt = f"({COLOR_YELLOW}{COLOR_BOLD}?{COLOR_RESET}) {prompt}. {COLOR_YELLOW}Ejemplo: {example}{COLOR_RESET}"
    return get_valid_int(formatted_prompt, min_val)

# ═══════════════════════════════════════════════════════════
# SECCIÓN 3: CLASES DE LÓGICA ESTADÍSTICA
# ═══════════════════════════════════════════════════════════

class ProbabilisticSolver:
    """Manejador de Teoría de Conjuntos y Probabilidades de Laplace."""
    def __init__(self):
        self.E: Set[Any] = set()
        self.events: Dict[str, Set[Any]] = {}

    def set_sample_space(self, elements: List[Any]):
        parsed = []
        for x in elements:
            try:
                parsed.append(int(x))
            except ValueError:
                parsed.append(x)
        self.E = set(parsed)
        self.events = {}

    def add_event(self, name: str, elements: Set[Any]):
        parsed_elements = set()
        for x in elements:
            try:
                parsed_elements.add(int(x))
            except ValueError:
                parsed_elements.add(x)
        self.events[name] = parsed_elements.intersection(self.E)

    def add_event_by_filter(self, name: str, condition: Callable[[Any], bool]):
        self.events[name] = {x for x in self.E if condition(x)}

    def get_intersection(self, name1: str, name2: str) -> Set[Any]:
        return self.events[name1].intersection(self.events[name2])

    def get_complement(self, name: str) -> Set[Any]:
        return self.E - self.events[name]

    def get_laplace_prob(self, name: str) -> float:
        if not self.E: return 0.0
        return len(self.events[name]) / len(self.E)

    def union(self, name1: str, name2: str) -> Set[Any]:
        return self.events[name1].union(self.events[name2])

    def difference(self, name1: str, name2: str) -> Set[Any]:
        return self.events[name1].difference(self.events[name2])

    def are_disjoint(self, name1: str, name2: str) -> bool:
        return self.events[name1].isdisjoint(self.events[name2])

    def get_full_analysis(self, name1: str, name2: str) -> Dict[str, Any]:
        inter = self.get_intersection(name1, name2)
        return {
            "interseccion": inter,
            "union": self.union(name1, name2),
            "diferencia": self.difference(name1, name2),
            "disjuntos": self.are_disjoint(name1, name2),
            "estado": "INCOMPATIBLES" if self.are_disjoint(name1, name2) else "COMPATIBLES"
        }

class SystematicSampler:
    """Generador de Muestreo Sistemático."""
    @staticmethod
    def generate(N: int, n: int, k: int = None, A: int = None) -> List[int]:
        if k is None:
            k = N // n
        if A is None:
            A = random.randint(1, k)
        sample = []
        for i in range(n):
            val = A + (i * k)
            if val <= N:
                sample.append(val)
        return sample

class SamplingAnalyzer:
    """Motor de análisis de tipos de muestreo y distribuciones."""
    @staticmethod
    def identify_type(description: str) -> tuple[str, str]:
        desc = description.lower()
        if any(word in desc for word in ["conveniencia", "primeros", "aceptaron", "disponibles"]):
            return "Muestreo por Conveniencia", "Se seleccionan los elementos que están más accesibles o disponibles para el investigador."
        if any(word in desc for word in ["sistemático", "intervalo", "cada k", "terminan en"]):
            return "Muestreo Sistemático", "Se selecciona un elemento aleatorio y luego cada k-ésimo elemento de la población."
        if any(word in desc for word in ["estratificado", "estratos", "secciones", "grupos"]):
            return "Muestreo Estratificado", "La población se divide en estratos homogéneos y se toma una muestra proporcional de cada uno."
        if any(word in desc for word in ["aleatorio simple", "tabla de números", "sorteo"]):
            return "Muestreo Aleatorio Simple", "Cada elemento de la población tiene la misma probabilidad de ser elegido."
        return "No identificado", "La descripción no coincide con los patrones comunes de muestreo."

    @staticmethod
    def calculate_stratified(strata_dict: Dict[str, int], total_sample_size: int) -> Dict[str, int]:
        total_pop = sum(strata_dict.values())
        if total_sample_size > total_pop:
            raise ValueError(f"Error Educativo: El tamaño de la muestra ({total_sample_size}) no puede ser mayor que la población total ({total_pop}).")
        results = {}
        for name, count in strata_dict.items():
            results[name] = int((count / total_pop) * total_sample_size)
        return results

    @staticmethod
    def calculate_proportion_distribution(N: int, n: int, p: float) -> Dict[str, Any]:
        if n > N:
            raise ValueError(f"Error Educativo: El tamaño de la muestra (n={n}) no puede ser mayor que la población (N={N}).")
        if not (0 <= p <= 1):
            raise ValueError(f"Error Educativo: La proporción poblacional (p={p}) debe estar entre 0 y 1.")

        mean = p
        std_error = math.sqrt((p * (1 - p) / n) * ((N - n) / (N - 1)))
        margin_error = 1.96 * std_error
        return {
            "media": mean,
            "desviacion_estandar": std_error,
            "intervalo_confianza": (mean - margin_error, mean + margin_error),
            "margen_error": margin_error
        }

# ═══════════════════════════════════════════════════════════
# SECCIÓN 4: FUNCIONES DE SIMULACIÓN
# ═══════════════════════════════════════════════════════════

def launch_coin() -> Any:
    return random.choice(["Cara", "Cruz"])

def launch_die() -> Any:
    return random.randint(1, 6)

def draw_numbered_ball() -> Any:
    return random.randint(1, 10)

def draw_colored_ball() -> Any:
    balls = ["Roja"] * 6 + ["Amarilla"] * 5 + ["Verde"] * 3
    return random.choice(balls)

# ═══════════════════════════════════════════════════════════
# SECCIÓN 5: FUNCIONES DE EXPORTACIÓN Y FORMATO
# ═══════════════════════════════════════════════════════════

def run_simulation(experiment_func: Callable[[], Any], n: int) -> Union[Any, Counter]:
    if n == 1:
        return experiment_func()
    return Counter(experiment_func() for _ in range(n))

def format_results(results: Counter):
    """Muestra los resultados de una simulación masiva en una tabla profesional."""
    total = sum(results.values())
    headers = ["Valor", "Frecuencia", "Porcentaje (%)"]
    rows = []
    for value, freq in sorted(results.items()):
        percentage = (freq / total) * 100
        rows.append([str(value), str(freq), f"{percentage:.2f}%"])
    draw_table(headers, rows)

def export_to_csv(experiment_name: str, results: Union[Counter, Dict[str, Any]], is_theoretical: bool = False) -> str:
    folder = ensure_results_folder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{experiment_name.replace(' ', '_')}_{timestamp}.csv"
    filepath = os.path.join(folder, filename)

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        f.write("sep=,\n")
        writer = csv.writer(f, delimiter=',')
        if is_theoretical:
            writer.writerow(["--- ANALISIS TEORICO ---"])
            writer.writerow(["Concepto", "Elementos", "Probabilidad/Resultado"])
            for key, val in results.items():
                writer.writerow([key, str(val), results.get(f"prob_{key}", "N/A")])
        else:
            writer.writerow(["--- RESULTADOS DE SIMULACION ---"])
            writer.writerow(['Valor', 'Frecuencia', 'Porcentaje (%)'])
            total = sum(results.values())
            for val, freq in sorted(results.items()):
                percentage = (freq / total) * 100
                writer.writerow([val, freq, f"{percentage:.2f}%"])
    return os.path.abspath(filepath)

def wait_for_user():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input(f"\n{COLOR_CYAN}Presione Enter para continuar...{COLOR_RESET}")

# ═══════════════════════════════════════════════════════════
# SECCIÓN 6: SUBMENÚS (Simulaciones, Sucesos, Muestreo, Actividades)
# ═══════════════════════════════════════════════════════════

def submenu_simulations():
    """Menú de simulaciones masivas para experimentos aleatorios."""
    simulations = {
        "1": ("Lanzar moneda", launch_coin),
        "2": ("Lanzar dado de 6 caras", launch_die),
        "3": ("Extraer bola de urna (1-10)", draw_numbered_ball),
        "4": ("Extraer bola de urna de colores", draw_colored_ball),
    }
    while True:
        draw_ui_header("MÓDULO DE SIMULACIONES", "SIMULACIONES")
        for k, (name, _) in simulations.items():
            print(f"{k}. {name}")
        print("0. Volver al menú")

        sub_opt = input(f"\n{COLOR_CYAN}Seleccione experimento (0-4): {COLOR_RESET}")
        if sub_opt == "0": break
        if sub_opt in simulations:
            name, func = simulations[sub_opt]
            n = get_didactic_int(f"¿Cuántas veces ejecutar {name}?", "100")
            result = run_simulation(func, n)
            if n == 1:
                print(f"\n{COLOR_GREEN}RESULTADO: {COLOR_BOLD}{result}{COLOR_RESET}")
            else:
                format_results(result)
                if didactic_prompt(f"\n{COLOR_CYAN}¿Exportar a Excel?", "[S/N]").upper() == 'S':
                    path = export_to_csv(name, result)
                    print(f"{COLOR_GREEN}✓ Exportado a: {COLOR_BOLD}{path}{COLOR_RESET}")
            wait_for_user()
        else:
            print(f"{COLOR_RED}Opción no válida.{COLOR_RESET}")
            wait_for_user()

def submenu_events(solver: ProbabilisticSolver):
    """Calculadora de sucesos basada en Teoría de Conjuntos."""
    while True:
        draw_ui_header("CALCULADORA DE SUCESOS (LÓGICA)", "SUCESOS")
        print(f"Espacio Muestral E: {COLOR_YELLOW}{solver.E if solver.E else 'No definido'}{COLOR_RESET}")
        print(f"Sucesos definidos: {list(solver.events.keys())}")
        print("\n1. Definir/Resetear Espacio Muestral (E)")
        print("2. Crear Suceso (A, B, C...) mediante filtro")
        print("3. Analizar Compatibilidad (Intersección)")
        print("4. Calcular Suceso Contrario (Complemento)")
        print("5. Calcular Probabilidad de Laplace")
        print("0. Volver al menú")

        sub_opt = input(f"\n{COLOR_CYAN}Opción: {COLOR_RESET}")
        if sub_opt == "0": break

        if sub_opt != "1" and not solver.E:
            print(f"\n{COLOR_RED}⚠️ Primero debes definir tu Espacio Muestral (Opción 1).{COLOR_RESET}")
            wait_for_user()
            continue

        if sub_opt == "1":
            raw_e = didactic_prompt("Ingrese elementos de E separados por coma", "1,2,roja,verde")
            solver.set_sample_space([x.strip() for x in raw_e.split(',')])
        elif sub_opt == "2":
            name = didactic_prompt("Nombre del suceso", "A")
            filter_type = didactic_prompt("Filtro: [1] Pares, [2] Impares, [3] Múltiplos de n, [4] Manual", "1")
            if filter_type == "1": solver.add_event_by_filter(name, lambda x: isinstance(x, int) and x % 2 == 0)
            elif filter_type == "2": solver.add_event_by_filter(name, lambda x: isinstance(x, int) and x % 2 != 0)
            elif filter_type == "3":
                n_mult = get_didactic_int("Ingrese el múltiplo n", "3")
                solver.add_event_by_filter(name, lambda x: isinstance(x, int) and x % n_mult == 0)
            elif filter_type == "4":
                elems = didactic_prompt("Ingrese elementos separados por coma", "2, 4, 6")
                parsed_elems = []
                for x in elems.split(','):
                    val = x.strip()
                    try: parsed_elems.append(int(val))
                    except ValueError: parsed_elems.append(val)
                solver.add_event(name, set(parsed_elems))
            print(f"{COLOR_GREEN}Suceso {name} creado con éxito.{COLOR_RESET}")
            wait_for_user()
        elif sub_opt == "3":
            n1 = didactic_prompt("Suceso 1", "A")
            n2 = didactic_prompt("Suceso 2", "B")
            if n1 in solver.events and n2 in solver.events:
                inter = solver.get_intersection(n1, n2)
                status = "COMPATIBLES" if inter else "INCOMPATIBLES"
                draw_table(["Intersección", "Estado"], [[f"{n1}∩{n2}: {inter}", status]])
            else: print(f"{COLOR_RED}Error: Sucesos no definidos.{COLOR_RESET}")
            wait_for_user()
        elif sub_opt == "4":
            name = didactic_prompt("Suceso a invertir", "A")
            if name in solver.events:
                comp = solver.get_complement(name)
                draw_table(["Suceso Contrario", "Elementos"], [[f"{name}'", comp]])
            else: print(f"{COLOR_RED}Error: Suceso no definido.{COLOR_RESET}")
            wait_for_user()
        elif sub_opt == "5":
            name = didactic_prompt("Suceso para Laplace", "A")
            if name in solver.events:
                prob = solver.get_laplace_prob(name)
                draw_table(["Suceso", "Probabilidad", "Porcentaje"], [[name, f"{prob:.4f}", f"{prob*100:.2f}%"]])
            else: print(f"{COLOR_RED}Error: Suceso no definido.{COLOR_RESET}")
            wait_for_user()
        else:
            print(f"{COLOR_RED}Opción no válida.{COLOR_RESET}")
            wait_for_user()

def submenu_systematic_sampling():
    """Generador de Muestreo Sistemático interactivo."""
    while True:
        draw_ui_header("GENERADOR DE MUESTREO SISTEMÁTICO", "MUESTREO")
        N = get_didactic_int("Población total (N)", "5000")
        while True:
            n = get_didactic_int("Tamaño de la muestra (n)", "100")
            if n <= N: break
            print(f"{COLOR_RED}Error: La muestra no puede ser mayor que la población.{COLOR_RESET}")

        k = N // n
        print(f"\n{COLOR_CYAN}Intervalo calculado (k): {COLOR_BOLD}{k}{COLOR_RESET}")
        choice = didactic_prompt("¿Cómo desea elegir el primer elemento? [Manual/Azar]", "Azar").strip().lower()
        A = get_didactic_int(f"Ingrese el número inicial (A) entre 1 y {k}", "1") if choice == 'manual' else random.randint(1, k)
        if choice != 'manual': print(f"{COLOR_GREEN}Arranque aleatorio seleccionado: {A}{COLOR_RESET}")

        sample = SystematicSampler.generate(N, n, k, A)
        print(f"\n{COLOR_GREEN}Muestra generada sistemáticamente:{COLOR_RESET}")
        draw_table(["Índice", "Valor Elemento"], [[i+1, val] for i, val in enumerate(sample)])

        if didactic_prompt(f"\n{COLOR_CYAN}¿Exportar muestra a Excel?", "[S/N]").upper() == 'S':
            path = export_to_csv("Muestreo_Sistematico", {"Muestra": sample}, is_theoretical=True)
            print(f"{COLOR_GREEN}✓ Exportado a: {COLOR_BOLD}{path}{COLOR_RESET}")

        if didactic_prompt("\n¿Desea generar otra muestra o volver?", "[V/N]").upper() == 'V':
            break
        wait_for_user()

def submenu_guided_activities():
    """Módulo de actividades guiadas para aprendizaje de estadística."""
    while True:
        draw_ui_header("GUÍA DE RESOLUCIÓN: TALLER DE ESTADÍSTICA", "ACTIVIDADES")
        print(f"{COLOR_YELLOW}{COLOR_BOLD}ESTADO: Modo Demostrativo.{COLOR_RESET}")
        print(f"{COLOR_YELLOW}Estas actividades utilizan los motores lógicos de Stat-Sim Pro para{COLOR_RESET}")
        print(f"{COLOR_YELLOW}resolver los ejercicios específicos del taller de Grado 9º.{COLOR_RESET}\n")
        print("1. Actividad 1 - Espacios Muestrales")
        print("2. Actividad 2 - Sucesos y Compatibilidad")
        print("3. Actividad 3 - Análisis de Dados")
        print("4. Actividad 4 - Ruleta (16 sectores)")
        print("5. Actividad 5 - Tipos de Muestreo")
        print("0. Volver al menú")

        sub_opt = input(f"\n{COLOR_CYAN}Seleccione actividad (0-5): {COLOR_RESET}")
        if sub_opt == "0": break

        # Delegación a funciones de actividad
        if sub_opt == "1": activity_1_sample_spaces()
        elif sub_opt == "2": activity_2_events_and_compatibility()
        elif sub_opt == "3": activity_3_dice_analysis()
        elif sub_opt == "4": activity_4_roulette()
        elif sub_opt == "5": activity_5_sampling_types()
        else:
            print(f"{COLOR_RED}Opción no válida.{COLOR_RESET}")
            wait_for_user()

# ═══════════════════════════════════════════════════════════
# SECCIÓN 7: FUNCIONES DE ACTIVIDADES
# ═══════════════════════════════════════════════════════════

def activity_1_sample_spaces():
    """Actividad 1: Ejercicios de definición de espacios muestrales."""
    draw_ui_header("ACTIVIDAD 1: ESPACIOS MUESTRALES", "ACTIVIDADES")
    print(f"{COLOR_BOLD}Enunciado:{COLOR_RESET} Definir el espacio muestral de los siguientes experimentos.")

    solver = ProbabilisticSolver()
    casos = {
        "a) Lanzar una moneda": ["Cara", "Sello"],
        "b) Lanzar un dado": [1, 2, 3, 4, 5, 6],
        "c) Extraer bola de urna (1-10)": list(range(1, 11)),
        "d) Urna de colores (6R, 5A, 3V)": [f"R{i}" for i in range(1, 7)] + [f"A{i}" for i in range(1, 6)] + [f"V{i}" for i in range(1, 4)]
    }

    results_table = []
    for desc, elements in casos.items():
        print(f"\n{COLOR_YELLOW}[INFO] Procesando caso: {desc}...{COLOR_RESET}")
        solver.set_sample_space(elements)
        results_table.append([desc, f"E = {solver.E}"])

    print(f"\n{COLOR_GREEN}RESULTADOS CONSOLIDADOS:{COLOR_RESET}")
    draw_table(["Experimento", "Espacio Muestral (E)"], results_table)

    if didactic_prompt(f"\n{COLOR_CYAN}¿Exportar resultados a Excel?", "[S/N]").upper() == 'S':
        path = export_to_csv("Actividad1_Espacios", {"Caso": [r[0] for r in results_table], "Espacio": [r[1] for r in results_table]}, is_theoretical=True)
        print(f"{COLOR_GREEN}✓ Exportado a: {COLOR_BOLD}{path}{COLOR_RESET}")

    wait_for_user()

def activity_2_events_and_compatibility():
    """Actividad 2: Análisis de sucesos y compatibilidad."""
    draw_ui_header("ACTIVIDAD 2: SUCESOS Y COMPATIBILIDAD", "ACTIVIDADES")
    print(f"{COLOR_BOLD}Enunciado:{COLOR_RESET} Dado E={{1..10}}, analizar sucesos A={{2,3,6}}, B={{1,5,9,10}}, C={{2,5}}.")

    print(f"\n{COLOR_YELLOW}[INFO] Configurando ProbabilisticSolver y definiendo sucesos...{COLOR_RESET}")
    solver = ProbabilisticSolver()
    solver.set_sample_space(list(range(1, 11)))
    solver.add_event("A", {2, 3, 6})
    solver.add_event("B", {1, 5, 9, 10})
    solver.add_event("C", {2, 5})

    # Análisis de Compatibilidad
    comparaciones = [("A", "B"), ("B", "C"), ("A", "C")]
    compat_results = []
    for n1, n2 in comparaciones:
        disjoint = solver.are_disjoint(n1, n2)
        status = "Incompatibles (Disjuntos)" if disjoint else "Compatibles"
        compat_results.append([f"{n1} y {n2}", status])

    print(f"\n{COLOR_GREEN}ANÁLISIS DE COMPATIBILIDAD:{COLOR_RESET}")
    draw_table(["Sucesos", "Estado"], compat_results)

    # Complementos
    print(f"\n{COLOR_YELLOW}[INFO] Calculando sucesos contrarios (Complementos)...{COLOR_RESET}")
    comp_results = []
    for name in ["A", "B", "C"]:
        comp_results.append([f"{name}'", solver.get_complement(name)])

    print(f"\n{COLOR_GREEN}SUCESOS CONTRARIOS:{COLOR_RESET}")
    draw_table(["Sucesos", "Elementos"], comp_results)

    if didactic_prompt(f"\n{COLOR_CYAN}¿Exportar análisis a Excel?", "[S/N]").upper() == 'S':
        path = export_to_csv("Actividad2_Sucesos", {"Sucesos": ["A", "B", "C"], "Complementos": [str(r) for r in [solver.get_complement("A"), solver.get_complement("B"), solver.get_complement("C")]]}, is_theoretical=True)
        print(f"{COLOR_GREEN}✓ Exportado a: {COLOR_BOLD}{path}{COLOR_RESET}")

    wait_for_user()

def activity_3_dice_analysis():
    """Actividad 3: Análisis avanzado de lanzamientos de dados."""
    draw_ui_header("ACTIVIDAD 3: ANÁLISIS DE DADOS", "ACTIVIDADES")
    print(f"{COLOR_BOLD}Enunciado:{COLOR_RESET} Sobre E={{1..6}}, analizar múltiplos de 2 y 3, y el contrario de 'menor que 5'.")

    solver = ProbabilisticSolver()
    solver.set_sample_space(list(range(1, 7)))

    print(f"\n{COLOR_YELLOW}[INFO] Generando sucesos mediante comprensión de listas...{COLOR_RESET}")
    s1_elements = {x for x in solver.E if x % 2 == 0}
    s2_elements = {x for x in solver.E if x % 3 == 0}

    solver.add_event("Múltiplos de 2", s1_elements)
    solver.add_event("Múltiplos de 3", s2_elements)

    # Compatibilidad
    is_disjoint = solver.are_disjoint("Múltiplos de 2", "Múltiplos de 3")
    inter = solver.get_intersection("Múltiplos de 2", "Múltiplos de 3")

    print(f"\n{COLOR_GREEN}RESULTADOS DE COMPATIBILIDAD:{COLOR_RESET}")
    draw_table(["Análisis", "Resultado"], [
        ["S1 ∩ S2", inter],
        ["Estado", "Incompatibles" if is_disjoint else "Compatibles"]
    ])

    # Suceso Contrario de 'menor que 5'
    print(f"\n{COLOR_YELLOW}[INFO] Calculando el contrario de 'Sucesos menores que 5'...{COLOR_RESET}")
    s3_elements = {x for x in solver.E if x < 5}
    solver.add_event("Menores que 5", s3_elements)
    contrario_s3 = solver.get_complement("Menores que 5")

    print(f"\n{COLOR_GREEN}RESULTADO CONTRARIO:{COLOR_RESET}")
    print(f"Sucesos menores que 5: {s3_elements}")
    print(f"Suceso Contrario (S3'): {COLOR_BOLD}{contrario_s3}{COLOR_RESET}")

    if didactic_prompt(f"\n{COLOR_CYAN}¿Exportar resultados a Excel?", "[S/N]").upper() == 'S':
        path = export_to_csv("Actividad3_Dados", {"Concepto": ["Intersección", "S3'"], "Valor": [str(inter), str(contrario_s3)]}, is_theoretical=True)
        print(f"{COLOR_GREEN}✓ Exportado a: {COLOR_BOLD}{path}{COLOR_RESET}")

    wait_for_user()

def activity_4_roulette():
    """Actividad 4: Ruleta y Probabilidad de Laplace."""
    draw_ui_header("ACTIVIDAD 4: RULETA Y PROBABILIDADES", "ACTIVIDADES")
    print(f"{COLOR_BOLD}Enunciado:{COLOR_RESET} Calcular probabilidades en una ruleta de 16 sectores y analizar compatibilidad.")

    solver = ProbabilisticSolver()
    omega = list(range(1, 17))
    solver.set_sample_space(omega)

    print(f"\n{COLOR_YELLOW}[INFO] Definiendo sucesos mediante filtros lógicos...{COLOR_RESET}")
    # Definición de sucesos
    sucesos_defs = {
        "Par": {x for x in omega if x % 2 == 0},
        "Impar": {x for x in omega if x % 2 != 0},
        "Múltiplo 6": {x for x in omega if x % 6 == 0},
        "Múltiplo 5": {x for x in omega if x % 5 == 0},
        "Múltiplo 4": {x for x in omega if x % 4 == 0},
        "Múltiplo 3": {x for x in omega if x % 3 == 0}
    }

    # Agregar al solver para usar sus métodos
    for name, elems in sucesos_defs.items():
        solver.add_event(name, elems)

    # 1. Cálculos de Probabilidades
    prob_results = []
    for name, elems in sucesos_defs.items():
        prob = solver.get_laplace_prob(name)
        # Representación de fracción simple
        frac = f"{len(elems)}/16"
        prob_results.append([name, f"{elems}", f"{prob:.4f}", frac])

    print(f"\n{COLOR_GREEN}PROBABILIDADES DE LAPLACE (P = |S| / |E|):{COLOR_RESET}")
    draw_table(["Suceso", "Elementos", "Prob. Decimal", "Fracción"], prob_results)

    # 2. Matriz de Compatibilidad Cruzada
    print(f"\n{COLOR_YELLOW}[INFO] Realizando análisis de compatibilidad cruzada...{COLOR_RESET}")
    names = list(sucesos_defs.keys())
    compatibilidad = []

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            disjoint = solver.are_disjoint(n1, n2)
            status = f"{COLOR_GREEN}COMPATIBLES{COLOR_RESET}" if not disjoint else f"{COLOR_RED}INCOMPATIBLES{COLOR_RESET}"
            compatibilidad.append([f"{n1} ∩ {n2}", status])

    # Para la tabla no podemos usar colores internos fácilmente, imprimiremos la lista
    print(f"\n{COLOR_GREEN}RESULTADOS DE COMPATIBILIDAD:{COLOR_RESET}")
    for pair, status in compatibilidad:
        print(f" {pair}: {status}")

    # 3. Caso de Muestreo Sistemático
    print(f"\n{COLOR_BOLD}--- CASO DE MUESTREO SISTEMÁTICO ---{COLOR_RESET}")
    print(f"Población (N): 5000 | Muestra (n): 100 | Intervalo (k): 50")
    print(f"{COLOR_YELLOW}[INFO] Generando serie de muestreo empezando en A=24...{COLOR_RESET}")

    A = 24
    k = 50
    muestra_inicio = []
    for i in range(5):
        val = A + (i * k)
        muestra_inicio.append(val)

    print(f"\n{COLOR_GREEN}Primeros 5 elementos de la muestra:{COLOR_RESET}")
    print(f"{COLOR_BOLD}{muestra_inicio}{COLOR_RESET}")
    print(f"Sucesión: 24, 74, 124, 174, 224...")

    if didactic_prompt(f"\n{COLOR_CYAN}¿Exportar reporte de Ruleta a Excel?", "[S/N]").upper() == 'S':
        # Exportamos las probabilidades
        path = export_to_csv("Actividad4_Ruleta", {"Suceso": [r[0] for r in prob_results], "Prob": [r[2] for r in prob_results]}, is_theoretical=True)
        print(f"{COLOR_GREEN}✓ Exportado a: {COLOR_BOLD}{path}{COLOR_RESET}")

    wait_for_user()

def activity_5_sampling_types():
    """Actividad 5: Clasificación y cálculo de muestreos."""
    draw_ui_header("ACTIVIDAD 5: TIPOS DE MUESTREO", "ACTIVIDADES")
    print(f"{COLOR_BOLD}Objetivo:{COLOR_RESET} Resolver los casos de identificación y cálculo de muestreo del taller.")

    analyzer = SamplingAnalyzer()

    # 1. Clasificación de Casos (a, b, d, f)
    print(f"\n{COLOR_BOLD}--- PARTE 1: Identificación de Muestreos ---{COLOR_RESET}")
    casos_texto = {
        "a) Arquitectos": "Se eligieron los primeros 20 arquitectos que aceptaron participar en la encuesta.",
        "b) Facturas": "Se seleccionaron 50 facturas tomando cada 10ma factura de la lista.",
        "d) Libros": "Se dividió la población de libros en secciones y se tomó una muestra proporcional de cada una.",
        "f) Opinión Política": "Se realizó un sorteo mediante una tabla de números aleatorios para elegir la muestra."
    }

    print(f"{COLOR_YELLOW}[INFO] Analizando descripciones mediante 'SamplingAnalyzer.identify_type()'...{COLOR_RESET}")
    ident_results = []
    for id_caso, texto in casos_texto.items():
        tipo, motivo = analyzer.identify_type(texto)
        ident_results.append([id_caso, tipo, motivo])

    draw_table(["Caso", "Tipo Identificado", "Justificación"], ident_results)

    # 2. Muestreo Estratificado (Punto c)
    print(f"\n{COLOR_BOLD}--- PARTE 2: Muestreo Estratificado (Caso c) ---{COLOR_RESET}")
    print("Enunciado: Empresa con 600 trabajadores divididos en A=200, B=150, C=150, D=100. Muestra n=20.")

    strata = {"Sección A": 200, "Sección B": 150, "Sección C": 150, "Sección D": 100}
    n_total = 20

    print(f"{COLOR_YELLOW}[INFO] Ejecutando 'SamplingAnalyzer.calculate_stratified()'...{COLOR_RESET}")
    res_strat = analyzer.calculate_stratified(strata, n_total)

    strat_table = []
    for section, pop in strata.items():
        strat_table.append([section, pop, res_strat[section]])

    draw_table(["Sección", "Población", "Muestra Asignada"], strat_table)

    # 3. Distribución de Proporción (Punto e)
    print(f"\n{COLOR_BOLD}--- PARTE 3: Distribución de Proporción (Caso e) ---{COLOR_RESET}")
    print("Enunciado: N=500, n=100, p=0.26 (proporción de mujeres).")

    print(f"{COLOR_YELLOW}[INFO] Ejecutando 'SamplingAnalyzer.calculate_proportion_distribution()'...{COLOR_RESET}")
    try:
        res_prop = analyzer.calculate_proportion_distribution(500, 100, 0.26)

        prop_table = [
            ["Media (p)", f"{res_prop['media']:.4f}"],
            ["Error Estándar", f"{res_prop['desviacion_estandar']:.4f}"],
            ["Margen de Error (95%)", f"{res_prop['margen_error']:.4f}"],
            ["Intervalo Confianza", f"{res_prop['intervalo_confianza'][0]:.4f} a {res_prop['intervalo_confianza'][1]:.4f}"]
        ]
        draw_table(["Métrica", "Valor"], prop_table)
    except ValueError as e:
        print(f"{COLOR_RED}Error en cálculo de proporción: {e}{COLOR_RESET}")

    if didactic_prompt(f"\n{COLOR_CYAN}¿Exportar reporte final de muestreo a Excel?", "[S/N]").upper() == 'S':
        path = export_to_csv("Actividad5_Muestreo_Final", {"Metricas": ["Estratificado", "Proporcion"], "Resultado": ["Calculado", "Calculado"]}, is_theoretical=True)
        print(f"{COLOR_GREEN}✓ Exportado a: {COLOR_BOLD}{path}{COLOR_RESET}")

    wait_for_user()

# ═══════════════════════════════════════════════════════════
# SECCIÓN 8: MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════

def main_menu():
    """Punto central de navegación del programa."""
    solver = ProbabilisticSolver()
    while True:
        draw_ui_header("MENÚ PRINCIPAL DE INGENIERÍA ESTADÍSTICA", "PRINCIPAL")
        print_banner()
        print(f"{COLOR_CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{COLOR_RESET}")
        print(f"{COLOR_CYAN}1. 🎲 Simulaciones Masivas{COLOR_RESET}")
        print(f"{COLOR_CYAN}2. 🧠 Calculadora de Sucesos (Teoría de Conjuntos){COLOR_RESET}")
        print(f"{COLOR_CYAN}3. 📏 Generador de Muestreo Sistemático{COLOR_RESET}")
        print(f"{COLOR_CYAN}4. 📚 Guía de Resolución: Taller de Estadística (Casos de Estudio){COLOR_RESET}")
        print(f"{COLOR_CYAN}5. 🚪 Salir{COLOR_RESET}")
        print(f"{COLOR_CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{COLOR_RESET}")

        option = input(f"\n{COLOR_CYAN}Seleccione un módulo (1-5): {COLOR_RESET}")

        if option == "5":
            print(f"\n{COLOR_YELLOW}Saliendo de STAT-SIM PRO...{COLOR_RESET}")
            break
        elif option == "1": submenu_simulations()
        elif option == "2": submenu_events(solver)
        elif option == "3": submenu_systematic_sampling()
        elif option == "4": submenu_guided_activities()
        else:
            print(f"{COLOR_RED}Opción no válida.{COLOR_RESET}")
            wait_for_user()

# ═══════════════════════════════════════════════════════════
# SECCIÓN 9: PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        setup_environment()
        main_menu()
    except Exception as e:
        print(f"{COLOR_RED}El programa se ha cerrado debido a un error crítico: {e}{COLOR_RESET}")
        input("\nPresione Enter para cerrar la ventana...")
