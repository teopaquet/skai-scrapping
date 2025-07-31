# Documentation de l’interface Skai Visualizer (Refine)

## Présentation générale

L’interface Skai Visualizer est une application web développée avec le framework Refine, utilisant Material UI pour le design et React Router pour la navigation. Elle permet de visualiser, gérer et explorer différentes ressources liées à l’aviation, telles que les données LinkedIn, les employés et les flottes d’avions.

---

## Navigation principale

L’application est structurée autour de plusieurs ressources principales accessibles via le menu latéral :

- **Home** : Page d’accueil de l’application.
- **Linkedin** : Section regroupant les données issues de LinkedIn, divisée en :
  - Airline’s Linkedin : Données LinkedIn des compagnies aériennes (CRUD complet).
  - Employee’s Linkedin : Données LinkedIn des employés (CRUD complet).
- **Fleet** : Données sur les flottes d’avions (CRUD complet).

Chaque ressource dispose d’icônes distinctives pour une navigation intuitive.

---

## Fonctionnalités principales

### 1. Layout et Thèmes

- Utilisation de `ThemedLayoutV2` et `ThemedSiderV2` pour un affichage moderne et responsive.
- Support du mode sombre/clair via le `ColorModeContextProvider`.
- Styles globaux appliqués pour une meilleure lisibilité.

### 2. Notifications et Feedback

- Système de notifications intégré (`RefineSnackbarProvider`) pour informer l’utilisateur des actions réalisées (création, modification, suppression, erreurs, etc.).

### 3. Navigation et Sécurité

- Navigation basée sur React Router, avec gestion des routes imbriquées.
- Protection contre la perte de modifications non sauvegardées (`UnsavedChangesNotifier`).
- Gestion dynamique du titre de la page selon la ressource consultée.

### 4. Accès rapide et productivité

- Intégration de la barre de commandes Refine Kbar (`RefineKbar`) pour une navigation et des actions rapides via le clavier.
- Outils de développement activés pour le suivi et le debug (`DevtoolsProvider`).

---

## Structure des ressources

Chaque ressource est définie avec les propriétés suivantes :

- **name** : Nom technique de la ressource.
- **list** : Chemin d’accès à la liste des éléments.
- **create/edit/show** : Chemins pour créer, éditer ou afficher un élément (si applicable).
- **meta** : Métadonnées pour l’affichage (label, icône, parent, suppression possible).

Exemple pour Airline’s Linkedin :
```js
{
  name: "Airline's Linkedin",
  list: "/linkedin",
  create: "/linkedin/create",
  edit: "/linkedin/edit/:id",
  show: "/linkedin/show/:id",
  meta: {
    label: "Airline's Linkedin",
    parent: "Linkedin",
    canDelete: true,
    icon: <LinkedInIcon />
  },
}
```

---

## Pages et routes

- `/` : Accueil
- `/linkedin` : Liste des compagnies aériennes LinkedIn
- `/employee` : Liste des employés LinkedIn
- `/fleet` : Liste des flottes d’avions
- `*` : Page d’erreur personnalisée

---

## Composants personnalisés

- **CustomSider** : Menu latéral personnalisé pour la navigation.
- **DrawerProvider** : Gestion des tiroirs (drawers) pour l’affichage de contenus contextuels.

---

## Sécurité et robustesse

- Gestion des erreurs via un composant dédié (`ErrorComponent`).
- Synchronisation de l’état de l’application avec l’URL pour un partage et une navigation cohérents.

---

## Extensibilité

L’architecture permet d’ajouter facilement de nouvelles ressources ou pages en modifiant la configuration des ressources dans `App.tsx`.

---

## Conclusion

L’interface Skai Visualizer offre une expérience utilisateur moderne, intuitive et sécurisée pour la gestion de données aéronautiques, avec une navigation claire et des fonctionnalités avancées pour la productivité.

---

N’hésitez pas à demander une documentation technique pour les développeurs ou des guides d’utilisation spécifiques pour chaque ressource si besoin.
