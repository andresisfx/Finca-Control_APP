# Sistema de Autenticación y Seguridad (JWT)

Este documento explica cómo se implementó el módulo de seguridad en **FincaControlApp**, garantizando que las contraseñas estén encriptadas y que los usuarios solo puedan acceder a la información mediante un Token seguro.

---

## 🔄 1. El Flujo de Datos (Login Flow)

El proceso de autenticación sigue el estándar **OAuth2 con JWT**:

1. **Registro:** El usuario envía su correo y contraseña en texto plano (`123456`). El sistema encripta la contraseña y la guarda en la base de datos como un hash irreversible (`$2b$12$R9h...`).
2. **Login:** El usuario envía sus credenciales al endpoint `/api/v1/auth/login/access-token`.
3. **Verificación:** El backend busca al usuario por su correo y compara matemáticamente la contraseña enviada con el hash guardado.
4. **Firma:** Si coincide, el servidor genera un **JSON Web Token (JWT)** firmado con una llave secreta y se lo entrega al usuario.
5. **Acceso:** Para usar cualquier otro endpoint protegido (ej. Crear una Finca), el frontend del usuario debe enviar ese Token en la cabecera HTTP (`Authorization: Bearer <Token>`).

---

## 🔐 2. Hashing de Contraseñas

Nunca guardamos contraseñas en texto plano. Usamos la librería `passlib` con el algoritmo **bcrypt**. Todo esto vive en `app/core/security.py`.

### Código Clave en `security.py`
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Convierte "123456" en un hash seguro
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compara la contraseña ingresada con el hash de la base de datos
    return pwd_context.verify(plain_password, hashed_password)
```

### Aplicación en `user_service.py`
Cuando se crea un usuario nuevo, interceptamos la contraseña antes de guardarla en PostgreSQL:
```python
def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        # Aquí inyectamos la función de encriptación
        password=get_password_hash(user_in.password), 
        nombre=user_in.nombre
    )
    db.add(db_user)
    db.commit()
```

---

## 🎟️ 3. Generación del Token (JWT)

Si el usuario hace login correctamente, le devolvemos un Token. El token contiene un "payload" (carga útil) donde guardamos el identificador del usuario (su `UUID`), llamado `sub` (Subject).

### Código Clave en `security.py`
```python
from jose import jwt

def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Se firma usando la SECRET_KEY del archivo .env
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
```

---

## 🛡️ 4. Middleware de Protección (Dependencias)

Para proteger una ruta y exigir que el usuario esté logueado, usamos las **Dependencias de FastAPI** (`Depends`). Creamos un interceptor en `app/api/deps.py`.

### El Interceptor (`deps.py`)
Esta función se ejecuta **antes** de que el usuario llegue a la ruta final. 
1. Lee el Token.
2. Verifica que la firma sea válida y que no haya expirado.
3. Extrae el `UUID` y busca al usuario en la base de datos.
4. Retorna el objeto `User` si todo está bien (o lanza Error 401 si hay trampa).

```python
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/access-token")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id_str = payload.get("sub")
    
    user = db.get(User, user_id_str)
    return user
```

### Protegiendo Rutas en la Práctica (`finca_routes.py`)
Cualquier endpoint que reciba a `current_user = Depends(get_current_user)` quedará automáticamente bloqueado para usuarios sin token. Además, podemos usar ese objeto `current_user` para saber quién hizo la petición.

```python
@router.post("/", response_model=FincaOut)
def create_finca(
    finca_in: FincaCreate, 
    db: Session = Depends(get_db),
    # 👇 ESTA LÍNEA ES EL CANDADO MÁGICO 👇
    current_user: User = Depends(get_current_user) 
):
    # Ya no dependemos de que el frontend nos diga quién es el dueño.
    # Lo sacamos directamente del token, evitando que un hacker cree fincas a nombre de otro.
    finca_in.usuario_id = current_user.id
    
    return finca_service.create_finca(db=db, finca_in=finca_in)
```

## Resumen del Flujo de Datos y Configuración

Para entender perfectamente el flujo de autenticación (Login y JWT) en FastAPI, puedes leer el código en este orden:

### 1. Las Configuraciones (La base)
Empieza por `backend/.env` y luego ve a `app/config.py`.
* **¿Qué verás aquí?** Las variables secretas (`SECRET_KEY`, `ALGORITHM` y el tiempo de expiración). Sin esto, no hay criptografía posible. Es el ADN de la seguridad.

### 2. La Caja de Herramientas Criptográficas
Ve al archivo `app/core/security.py`.
* **¿Qué verás aquí?** Son funciones matemáticas puras, sin base de datos. Verás cómo `passlib` hace el hash de una contraseña, cómo verifica si una contraseña coincide con su hash, y cómo la librería `jose` empaqueta los datos en un Token JWT firmado.

### 3. La Lógica de Negocio (El cerebro)
Abre `app/services/user_service.py`.
* **¿Qué verás aquí?** Busca la función `authenticate_user`. Aquí es donde la base de datos se encuentra con la criptografía. El flujo es: "Busca el usuario por email -> Si existe, saca su hash de la BD -> Mándalo a `security.py` para ver si la contraseña escrita es correcta".

### 4. La Puerta de Entrada (El Login)
Abre `app/routes/auth_routes.py`.
* **¿Qué verás aquí?** El endpoint `POST /login/access-token`. Este es el lugar exacto que la app móvil o el frontend tocará. Recibe el "formulario" con correo y contraseña, se lo pasa a `user_service.py` y, si todo sale bien, usa `security.py` para crear el Token y devolvérselo al usuario en formato JSON.

### 5. El Guardián de las Rutas (El Portero)
Finalmente, ve a `app/api/deps.py`.
* **¿Qué verás aquí?** La función `get_current_user`. Este es el portero de la discoteca. Cuando el usuario intenta acceder a sus fincas, FastAPI ejecuta este archivo primero. El código toma el Token JWT de la cabecera HTTP, lo desencripta, verifica que no haya expirado, extrae el UUID del usuario y va a la base de datos a comprobar que el usuario siga existiendo.

**En Resumen:**
1. El usuario se registra (`user_service.py` -> `get_password_hash`).
2. El usuario hace Login (`auth_routes.py` -> `authenticate_user` -> `create_access_token`).
3. El usuario pide ver sus fincas mandando su Token.
4. El "Portero" (`deps.py`) lo detiene, revisa su Token, descubre quién es, y le permite pasar a `finca_routes.py`.
