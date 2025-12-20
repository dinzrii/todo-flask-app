# Containerized Task Management System

## Goal
This project was developed to address the problem of environment inconsistency during deployment. 
The goal was to ensure identical behavior across different systems using containerization.

## Technology Stack
- Python
- Flask
- Docker
- Nginx
- SQLite

## Architecture
Client -> Nginx -> Flask Application -> SQLite Database

## How to Run
1. Clone the repository
2. docker-compose up --build (or docker build & run)
