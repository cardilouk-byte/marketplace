# AgroShop - E-Commerce Django (Projet scolaire)

Site e-commerce complet style AgroShop (bleu #1e40af / orange #f97316), fait avec Django.
Paiement MonCash & NatCash, dashboard admin, notifications, CMS, page builder.

## Installation

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Site public : http://127.0.0.1:8000/
- Dashboard admin : http://127.0.0.1:8000/dashboard/ (compte staff requis)
- Admin Django : http://127.0.0.1:8000/admin/

## Apps

| App | Role |
|---|---|
| products | Category, Product, Review + pages Akèy/Boutique/Pwodwi |
| orders | Cart, CartItem, Order, OrderItem + checkout |
| payments | Payment (MonCash, NatCash, carte, cash) |
| accounts | Inscription, connexion, espace client |
| cms | FAQ, Blog, Contact |
| builder | Modeles de design (identite, couleurs, polices, sections, slider, versions) |
| dashboard | Dashboard admin complet (CRUD + configuration) |
| notifications | Notification + signaux (imel lè kòmand/peman) |

## Structure des donnees (cles etrangeres)

- Product.category -> Category
- Review.product -> Product, Review.user -> User
- Cart.user -> User (ou session) ; CartItem.cart -> Cart, CartItem.product -> Product
- Order.client -> User ; OrderItem.order -> Order, OrderItem.product -> Product
- Payment.order -> Order
- Notification.user -> User ; NotificationPreference.user -> User (OneToOne)
- MenuItem.parent -> MenuItem (self) ; DesignVersion.created_by -> User
