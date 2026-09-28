# PulseTrack V1.4 — SQLite

## 🇫🇷 Français

PulseTrack V1.4 est un **script de tracking avec backend Python/SQLite conçu pour être intégré à un site web existant**.

Il ne s'agit pas d'un site web complet destiné à remplacer votre infrastructure actuelle. PulseTrack fournit la partie backend nécessaire pour recevoir, traiter et stocker les données envoyées depuis les pages de votre site.

### Fonctionnement

PulseTrack repose sur :

- `server.py` pour le backend et les API ;
- `pulsetrack.db` pour le stockage persistant SQLite ;
- un système d'authentification pour protéger le Dashboard administrateur ;
- un script de tracking à intégrer aux pages du site à analyser.

Le principe général est :

```text
Votre site web
      │
      │ Script de tracking
      ▼
PulseTrack Backend
   (server.py)
      │
      ▼
  pulsetrack.db
      │
      ▼
Admin Dashboard
```

Le script de tracking doit être intégré au **frontend de votre site**, tandis que le serveur PulseTrack doit fonctionner côté **backend**.

Les informations collectées sont envoyées au backend PulseTrack puis enregistrées dans `pulsetrack.db`.

Le Dashboard administrateur permet ensuite de consulter les informations enregistrées.

### Intégration

PulseTrack doit être installé sur le serveur qui hébergera le backend de tracking.

Les dépendances Python nécessaires sont disponibles dans :

```text
requirements.txt
```

Le serveur principal est lancé avec :

```bash
python server.py
```

ou, selon l'environnement :

```bash
python3 server.py
```

Pour une utilisation réelle sur Internet, PulseTrack doit être intégré à votre infrastructure serveur et configuré avec votre domaine.

Il est recommandé d'utiliser un **reverse proxy avec HTTPS** et de ne pas exposer directement le serveur de développement Python sur Internet.

### Base de données

PulseTrack utilise :

```text
pulsetrack.db
```

Il s'agit d'une base de données SQLite persistante.

Les données restent donc disponibles après :

- la fermeture du navigateur ;
- la déconnexion du Dashboard ;
- le redémarrage du backend PulseTrack.

### Sécurité et mise en production

Avant d'intégrer PulseTrack à un site accessible publiquement :

- changez `PULSETRACK_SECRET` ;
- changez les identifiants administrateur par défaut ;
- utilisez HTTPS ;
- configurez correctement votre serveur/reverse proxy ;
- ajoutez une limitation de débit et une protection contre les abus ;
- protégez l'accès au Dashboard administrateur ;
- définissez une politique de conservation des données ;
- informez les utilisateurs des données collectées ;
- obtenez et conservez le consentement lorsque celui-ci est requis par la réglementation applicable.

PulseTrack doit être considéré comme un **composant backend à intégrer et à configurer en fonction de l'infrastructure du site qui l'utilise**.

---

# 🇬🇧 English

PulseTrack V1.4 is a **Python/SQLite tracking backend designed to be integrated into an existing website**.

It is not intended to replace your existing website or infrastructure. PulseTrack provides the backend components required to receive, process, and store data sent from your website pages.

### How It Works

PulseTrack uses:

- `server.py` for the backend and APIs;
- `pulsetrack.db` for persistent SQLite storage;
- an authentication system to protect the Admin Dashboard;
- a tracking script that can be integrated into the website pages you want to analyze.

The general architecture is:

```text
Your Website
     │
     │ Tracking Script
     ▼
PulseTrack Backend
   (server.py)
     │
     ▼
 pulsetrack.db
     │
     ▼
Admin Dashboard
```

The tracking script is integrated into your website's **frontend**, while the PulseTrack server runs on the **backend**.

Collected information is sent to the PulseTrack backend and stored inside `pulsetrack.db`.

The Admin Dashboard can then be used to access the stored information.

### Integration

PulseTrack must be installed on the server that will host the tracking backend.

The required Python dependencies are listed in:

```text
requirements.txt
```

The main backend can be started with:

```bash
python server.py
```

or, depending on the environment:

```bash
python3 server.py
```

For production use, PulseTrack should be integrated into your server infrastructure and configured to work with your domain.

It is recommended to use a **reverse proxy with HTTPS** rather than exposing the Python development server directly to the Internet.

### Database

PulseTrack uses:

```text
pulsetrack.db
```

This is a persistent SQLite database.

Stored data therefore remains available after:

- closing the browser;
- logging out of the Admin Dashboard;
- restarting the PulseTrack backend.

### Security and Production Deployment

Before integrating PulseTrack into a publicly accessible website:

- change `PULSETRACK_SECRET`;
- change the default administrator credentials;
- use HTTPS;
- properly configure your server/reverse proxy;
- implement rate limiting and abuse protection;
- protect access to the Admin Dashboard;
- define a data retention policy;
- inform users about