# Proyecto_Herramientas - AutoMarket Perú

Plataforma de venta de autos con sistema de seguimiento de incidentes, CI/CD y despliegue en la nube.

## Arquitectura del proyecto

```
[Usuario]
    |  HTTPS
[GitHub Pages] ..................... Frontend estático (HTML/CSS/JS)
    |  API REST
[Render / Railway] ................. Backend Flask (Incidentes API)
    |
[SQLite / PostgreSQL] .............. Base de datos
```

## Tecnologías

- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Backend:** Python + Flask + SQLite
- **CI/CD:** GitHub Actions
- **Cloud:** GitHub Pages (frontend) + Render (backend)
- **Calidad:** Lighthouse CI

## Estructura del proyecto

```
├── backend/
│   ├── app.py                  API Flask de incidentes
│   └── requirements.txt        Dependencias Python
├── .github/workflows/
│   ├── stats.yml               Estadísticas diarias del proyecto
│   ├── lighthouse.yml          Auditoría Lighthouse CI
│   └── deploy.yml              Deploy a GitHub Pages
├── Login-register/
│   ├── login.html / login.css
│   └── register.html / register.css
├── navbar/
│   └── navbar.css
├── main/
│   └── daniel.css
├── Roadmap/
│   ├── stats.py                Generador de estadísticas
│   └── stats.md                Reporte generado automáticamente
├── incidentes.html             Dashboard de incidentes
├── incidentes.css              Estilos del dashboard
├── index.html                  Página principal
├── styles.css                  Estilos globales
├── footer.css                  Estilos del footer
├── render.yaml                 Config de deploy en Render
└── .lighthouserc.json          Config de Lighthouse CI
```

## Funcionalidades

### Semana 12 - Sistema de Seguimiento de Incidentes
- API REST full CRUD (Flask + SQLite)
- Dashboard web con tabla de incidentes
- Filtros por estado, categoría y prioridad
- Cards resumen (abiertos, en progreso, resueltos, total)
- Modal para crear y editar incidentes
- Categorías: Bug, Mejora, Incidente
- Prioridades: Baja, Media, Alta, Crítica
- Estados: Abierto, En Progreso, Resuelto, Cerrado

### Semana 13 - Integración Continua (CI)
- Workflow Lighthouse CI en cada push/PR
- Auditoría de rendimiento, accesibilidad, buenas prácticas y SEO
- Reporte HTML descargable como artifact

### Semana 14 - Entrega Continua (CD)
- Deploy automático a GitHub Pages en cada push a master
- URL pública: `https://fritz-13.github.io/herramientas-de-desarrollo-practica`

### Semana 15 - Plataformas en la Nube
- Frontend: GitHub Pages (CDN global, HTTPS gratis)
- Backend: Render (servicio web gestionado)
- Configuración declarativa via `render.yaml`
- Backend accesible en `https://herramientas-de-desarrollo-practica.onrender.com`

## Cómo ejecutar localmente

### Frontend
```bash
# Servir archivos estáticos
npx http-server . -p 8080
# Abrir http://localhost:8080
```

### Backend (Incidentes API)
```bash
cd backend
pip install -r requirements.txt
python app.py
# API en http://127.0.0.1:5000
```

### Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/incidentes` | Listar todos los incidentes |
| GET | `/api/incidentes/<id>` | Obtener un incidente |
| POST | `/api/incidentes` | Crear incidente |
| PUT | `/api/incidentes/<id>` | Actualizar incidente |
| DELETE | `/api/incidentes/<id>` | Eliminar incidente |

## CI/CD Pipeline

1. **Push a master** → Trigger workflows
2. **Lighthouse CI** → Auditoría de calidad
3. **Stats** → Actualización de estadísticas
4. **Deploy** → Publicación en GitHub Pages
5. **Resultado** → Sitio actualizado en minutos
