# GUI for IPN hand annotation (box_selectc.py)

#### General
* **[Ctr+O]**	Open bad box frame el TXT file
* **[Ctr+Q]**	Close the program

- **['Backspace', 'Caps', ']', A]**	Manda el bbox seleccionado a "selected_boxes" desde cualquier MODE.
- **[E]**	    Manda a None la seleccion de posibles bboxes.
- **[Q]**	    Selecciona el bbox de BBOX_1. Si ya esta activado BBOX_1, entonces cambia las sub_boxes.
- **[W]**	    Selecciona el bbox de BBOX_2. Si ya esta activado BBOX_2, entonces cambia las sub_boxes.
- **[R]**	    Selecciona TODOS los bboxes del BBOX activado.
- **[1]**	    Selecciona la caja 1 del BBOX activado. Diferente si esta en Change MODE.
- **[2]**	    Selecciona la caja 2 del BBOX activado. Diferente si esta en Change MODE.
- **[3]**	    Selecciona la caja 3 del BBOX activado.
- **[4]**	    Selecciona la caja 4 del BBOX activado.
- **[Z]**	    Copia el txt del frame anterior.
- **[Shf+Z]**	Copia el txt del frame siguiente.
- **[F]**	    Elimina el txt de frame actual.

#### Navegacion
- **[P]**	    Muestra el siguiente frame con anotaciones.
- **[O]**	    Muestra el frame anterior con anotaciones.
- **[M]**	    Genera el reporte general de los segmentos(clases) de todo el video.
- **[L]**	    Muestra el siguiente frame en CLEAN mode.
- **[Shf+L]**   Reproduce todos los frames en CLEAN mode.
- **[K]**	    Muestra el frame anterior en CLEAN mode.
- **[Shf+K]**	Reproduce en reversa todos los frames en CLEAN mode.
- **[S]**	    Detiene la repodrudccion de frames SOLO si se estan reproduciendo.


#### CHANGE MODE
- **[S]** 	    Entra a CHANGE mode desde CLEAN mode, o modifica la altura del bbox seleccionado si estamos en CHANGE mode. Tambien funciona para entrar a CLEAN mode desde modo anotaciones.
- **[Shf+S]** 	Modifica la altulra del bbox seleccionado si estamos en CHANGE mode.
- **[D]** 	    Entra a CHANGE mode desde CLEAN mode, o modifica la altura del bbox seleccionado si estamos en CHANGE mode. Tambien funciona para entrar a CLEAN mode desde modo anotaciones.
- **[Shf+D]** 	Modifica la altulra del bbox seleccionado si estamos en CHANGE mode.
- **[X]** 	    Entra a CHANGE mode desde CLEAN mode, o modifica el ancho del bbox seleccionado si estamos en CHANGE mode. Tambien funciona para entrar a CLEAN mode desde modo anotaciones.
- **[Shf+X]** 	Modifica el ancho del bbox seleccionado si estamos en CHANGE mode.
- **[C]** 	    Entra a CHANGE mode desde CLEAN mode, o modifica el ancho del bbox seleccionado si estamos en CHANGE mode. Tambien funciona para entrar a CLEAN mode desde modo anotaciones.
- **[Shf+C]** 	Modifica el ancho del bbox seleccionado si estamos en CHANGE mode.
- **[Shf+A]**   AGREGA un NUEVO bbox para modificarlo directamente en CHANGE mode. (util para agregar una segunda mano a las anotaciones)
- **[F]**	    Elimina el bbox seleccionado (si estas en CHANGE mode, regresa a CLEAN mode).
- **[1]** 	    Selecciona la caja 1 del bbox seleccionado para hacer cambios (cuando hay 2 bboxes selected)
- **[2]** 	    Selecciona la caja 2 del bbox seleccionado para hacer cambios (cuando hay 2 bboxes selected)

# GUI for IPN hand annotation (image.py)

#### Buttons
- **BBOX BORRADO!!** 	Borrado o Inexistente [R]
- **BAD BBOX**		    Manda TXT a carpeta de revision y si no hay TXT genera uno vacio [K]
- **GOD BBOX**		    Elimina TXT del frame en la carpeta de revision [Q]
- **BBOX Copiado**		BBox copiado del frame anterior [Z] (solo si no existe el TXT actual)
- **CLASE A D0X**		Cambia la clase del frame a D0X [F]

#### Shortcuts
- **CLASE Cambiada**	Se cambio la clase por una en especifico que no es D0x [F1-F11: G1-G11, 1-2: B0A-B0B]
- **[P]**               Play video
- **[Shf+P]**           Play Fast
- **[L]**               Play back
- **[Shf+L]**           Play back fast
- **[S]**               Stop play
- **[M]**               Next frame
- **[N]**               Prev frame

# duplicar_bbox.py

- **bbox_file**         Debemos poner el path del txt maestro, el cual contiene la box que se va a copiar (Mano estatica)
- **frames_path**       Debemos de poner el path de los txt del video al cual le vamos a agregar cajas
- **frame_range**       Solamente debemos de agregar el numero del frame inicial y final a los que les vamos a pegar la box
   - No debemos de agregar ceros a la izquierda, por ejemplo si vamos agregar una box de los frames 000001 al 000200, solamente vamos a poner [1,200]

# Reglas para anotar

- Si se lleva a ver un nudillo de las manos inactivas se deben de anotar.
- Se deben de anotar todas las manos que esten visibles o reconocibles.
- Para las manos secundarias (que no estan haciendo el gesto) se debe de tener como minimo un IoU del 50% entre la mano y la caja.