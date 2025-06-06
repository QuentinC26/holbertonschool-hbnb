
# HBnB - Technical UML Documentation

## 1. Introduction

This document provides a comprehensive technical blueprint for the HBnB project. It compiles and explains the high-level architecture, the internal class structures of the business logic, and the operational workflows for various API calls. Its purpose is to guide the implementation, ensure architectural consistency, and serve as a reference for the development team throughout the project lifecycle.

## 2. High-Level Architecture

### High-Level Package Diagram

This diagram illustrates the three-layered architecture of the HBnB application:

* **Presentation Layer**: Manages user-facing interfaces such as APIs and web services.
* **Business Logic Layer**: Contains all the core models and logic that govern the application.
* **Persistence Layer**: Manages data storage, interaction with databases, and file storage systems.

**Pattern Used:** The architecture implements the **Facade Pattern** to abstract and simplify interactions between layers.

*Explanatory Notes:*

* Components are separated by concern to improve modularity.
* Layers communicate vertically only: Presentation -> Logic -> Persistence.
* Models in the logic layer depend on persistence but are unaware of presentation specifics.

## 3. Business Logic Layer - Class Diagram

### Class Diagram

This diagram models the four main entities in the business logic:

* **User**
* **Place**
* **Review**
* **Amenity**

Each class includes core attributes (e.g., `id`, `created_at`, `updated_at`) and essential methods, along with defined relationships.

*Descriptions:*

* **User**

  * Attributes: `id`, `email`, `password`, `created_at`, `updated_at`
  * Methods: `register()`, `login()`
  * Relations: One user can own multiple places and submit many reviews.

* **Place**

  * Attributes: `id`, `name`, `description`, `price_by_night`, `created_at`, `updated_at`, `user_id`
  * Methods: `create()`, `update()`
  * Relations: Belongs to one user, can have many reviews and amenities.

* **Review**

  * Attributes: `id`, `text`, `place_id`, `user_id`, `created_at`, `updated_at`
  * Methods: `submit()`
  * Relations: Linked to one user and one place.

* **Amenity**

  * Attributes: `id`, `name`, `created_at`, `updated_at`
  * Methods: `add_to_place()`
  * Relations: Many-to-many with Place.

*Rationale:*

* Design adheres to single responsibility and clear ownership.
* UUIDs ensure uniqueness.
* Associations promote reusability and relational integrity.

## 4. API Interaction Flow - Sequence Diagrams

### Sequence Diagram 1: User Registration

Participants: User, API, Business Logic, Database

* User sends registration request.
* API validates input and calls User.register().
* User model creates a new record in the database.
* Confirmation returned to the user.

### Sequence Diagram 2: Place Creation

Participants: User, API, Business Logic, Database

* Authenticated user sends place creation request.
* API validates and sends data to Place.create().
* Place is linked to user and saved in database.
* Success response is returned.

### Sequence Diagram 3: Review Submission

Participants: User, API, Business Logic, Database

* User sends a review for a place.
* API verifies authorization.
* Review model submits and saves the entry.
* Review is linked to the user and place.

### Sequence Diagram 4: Fetching Places

Participants: User, API, Business Logic, Database

* User requests places with filters.
* API passes query to business logic.
* Logic layer queries database.
* Filtered results returned to user.

*Explanation of Diagrams:*

* Clearly show the role of each layer.
* Emphasize separation of concerns.
* Highlight key operations and data flow.

## 5. Conclusion

This document consolidates all architectural and design decisions made in the modeling of the HBnB system. The high-level view, detailed class structures, and operation-specific diagrams ensure a shared understanding among contributors. This blueprint is critical for maintaining consistency, scalability, and maintainability as the project evolves.

