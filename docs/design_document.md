# Motorbike Cost Tracker Design Document

## Overview
Motorbike Cost Tracker is a Reflex-based web application for tracking acquisition, refurbishment, and sales performance of motorbikes. The app initializes a light-themed Reflex application, creates database tables, seeds example data, and registers route-protected pages for browsing, editing, and analyzing inventory. Authentication-gated navigation ensures most routes redirect unauthenticated users to the sign-in page.

## System Architecture
- **Framework**: Built with Reflex, combining declarative UI components and server-side state management.
- **Routing & Initialization**: `app/app.py` instantiates the Reflex app, ensures database setup, and registers pages with session checks to guard access.
- **Database**: SQLModel models persist users, motorbikes, and parts. Database setup also seeds an example admin user and sample inventory.
- **State Management**: Reflex state classes encapsulate business logic for authentication, inventory management, and analytics.
- **UI Composition**: A shared page layout component provides consistent header, navigation, and sign-out controls for all authenticated pages.

## Data Model
### UserDB
Stores user credentials (UUID primary key, email, password hash) with uniqueness constraints to support authentication workflows.

### MotorbikeDB
Represents a motorbike purchase with base cost, split investments for two partners (Tanya and Gerald), optional buyer attribution, sold status/value, and a flag to ignore a bike in aggregate calculations. A one-to-many relationship links to parts.

### PartDB
Captures individual part purchases associated with a motorbike, including source, buyer, and cost. Cascade rules ensure parts are removed when their parent motorbike is deleted.

## Database Bootstrapping
`app/db_setup.py` creates tables on startup and populates an admin user along with two example motorbikes and associated parts if they are not already present. This data provides immediate context for dashboards and analytics screens.

## State Management
### AuthState
Handles sign-up, sign-in, sign-out, and session verification. Validation prevents empty credentials, enforces unique emails, and hashes passwords with bcrypt. Successful authentication redirects to the landing route while failures surface toast notifications.

### MotorbikeState
Centralizes inventory data and UI state:
- Maintains cached motorbike dictionaries derived from SQLModel instances, including computed totals for parts and partner investments.
- Provides computed properties for total portfolio cost, projected sale values (doubling the cost of unsold bikes), actual profit from sold bikes, sorted views, and detail selection derived from router params.
- Loads all motorbikes and parts on demand, ensuring part forms default to the first unsold bike when available.
- Validates and persists new motorbikes, auto-balancing the initial cost with Tanya/Gerald contributions when necessary.
- Allows part creation for selected or specific bikes while preventing edits on sold units.
- Supports editing and deletion flows for motorbikes and parts, keeping in-memory state synchronized with database transactions and respecting ignore-from-calculations and sold constraints.

### AnalyticsState
Builds derived analytics from `MotorbikeState` data. It filters bikes by sold status, skips ignored inventory, sums partner investments, computes profit when a sale price is present, and assigns equal profit shares. Aggregate totals roll up investment and profit distributions across the filtered dataset.

## User Interface & Screen Flows
### Shared Layout
`app/components/layout.py` supplies a header with page title, sign-out button, logo placeholder, and navigation bar linking to All Motorbikes, Dashboard, and Analytics. All authenticated pages render within this layout for consistency.

### Landing Page
Offers a welcome message, sign-out action, and quick navigation cards to the Dashboard, All Motorbikes, and Analytics. It verifies the session on mount.

### Authentication Pages
- **Sign In**: Form card prompting for email and password, submitting to `AuthState.sign_in` and linking to account creation.
- **Sign Up**: Mirror form for registration, submitting to `AuthState.sign_up` and linking back to sign-in.

### Dashboard
Combines CRUD controls and high-level metrics:
- **Motorbike Form**: Form inputs for name, initial cost, Tanya/Gerald shares, and buyer selection. Submissions invoke `MotorbikeState.add_motorbike` and reset on success.
- **Part Form**: Supports both general and bike-specific part addition, with dropdowns for unsold bikes, validation, and automatic disabling when no targets exist.
- **Financial Summary**: Cards displaying total cost, projected sale, and actual profit using computed state values.
- **Motorbike & Parts Tables**: Detailed cards for each motorbike with nested parts table, edit/delete actions, and summary of total costs.

### Motorbikes List
Grid of cards highlighting each motorbike’s status, cost, part count, and sale info. “SOLD” and “IGNORED” badges provide quick context. Clicking navigates to the detail view. Page also exposes edit dialogs for motorbikes and parts.

### Motorbike Detail Page
Focuses on one motorbike:
- Displays status badges, buyer, sale price, and computed profit for sold bikes.
- Provides detailed parts table with edit/delete actions disabled once the bike is marked sold.
- Shows total, Tanya, and Gerald part investments alongside the combined motorbike cost.
- Embeds a contextual part form to add components when the bike is unsold.

### Analytics Page
Delivers business insights:
- Filter control to toggle between all, sold, or unsold bikes (defaulting to all on mount).
- Summary cards showing total investments and profit shares for Tanya and Gerald across the filtered set.
- Tabular breakdown per bike with columns for initial cost, buyer, total cost, partner investments, profit, profit shares, and sold status badges.

## Financial Calculations
- **Part & Investment Aggregation**: `_convert_motorbike_db_to_dict` sums all part costs per bike, splitting totals by buyer and combining with the base purchase price for a comprehensive motorbike cost basis.
- **Portfolio Metrics**: `MotorbikeState.total_cost` totals all non-ignored bike costs. `projected_sale` doubles the cost basis of unsold, non-ignored bikes to estimate potential revenue. `actual_profit` sums realized profits from sold, non-ignored bikes by subtracting total cost from sale value.
- **Motorbike Validation**: When adding a bike, if Tanya and Gerald contributions do not sum to the provided initial cost, the state resets the initial cost to their combined contributions to maintain accounting integrity.
- **Analytics Breakdown**: `AnalyticsState` composes per-bike investment totals for Tanya and Gerald, computes profit when a sale exists, and divides profit equally between them. Aggregated totals sum investments and profit shares across the filtered data set.
- **Detail Profit Display**: The motorbike detail page reiterates profit for sold bikes by comparing sale value to the total motorbike cost and exposes partner-specific part spending totals.
- **Dashboard Summary Binding**: Summary cards on the dashboard display the computed total cost, projected sale, and actual profit metrics in real time.

## Security & Validation Considerations
- Authentication requires hashed passwords and enforces unique emails. Session checks redirect unauthenticated users away from protected routes.
- Input validation prevents negative costs, empty names, and editing of sold bikes or parts associated with them.
- Ignore-from-calculations flag allows removing edge cases from aggregate metrics without deleting the underlying data.

## Future Enhancements
Potential improvements include configurable profit-sharing ratios, audit trails for cost changes, richer buyer management, and exporting analytics. Enhancing reporting to visualize trends or integrate external marketplaces could further support decision-making.
