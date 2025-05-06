CREATE DATABASE ferremas;

CREATE TABLE ferremas.product (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price INT(11) NOT NULL,
    type INT(11) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE ferremas.users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    pass VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO ferremas.product (name, price, type) VALUES

-- Herramientas Manuales
('Martillo Mango de Madera', 5990, 1),
('Destornillador de Punta Plana 6mm', 3490, 1),
('Llave Ajustable 8 pulgadas', 6990, 1),
('Serrucho para Madera 20"', 5990, 1),

-- Materiales Básicos
('Clavos de Acero 1 pulgada (100u)', 2990, 2),
('Plancha de MDF 18mm 122x244cm', 15990, 2),
('Cemento Portland 25kg', 5890, 2),
('Arena Fina 25kg', 2890, 2),

-- Equipos de Seguridad
('Casco de Seguridad Amarillo', 8990, 3),
('Guantes de Cuero para Construcción', 4990, 3),
('Lentes de Seguridad Transparentes', 1990, 3),
('Botas de Seguridad con Punta de Acero T42', 25990, 3),

-- Tornillos y Anclajes
('Tornillos Philips 3x20mm (50u)', 1890, 4),
('Tarugo Plástico 6mm (100u)', 1990, 4),
('Anclajes de Expansión M10 (4u)', 3990, 4),
('Tornillos para Madera 4x30mm (100u)', 2490, 4),

-- Fijaciones y Adhesivos
('Silicona Transparente 280ml', 3490, 5),
('Pega Epóxica 2 Componentes 50ml', 5490, 5),
('Cinta Doble Contacto 10m x 19mm', 2990, 5),
('Adhesivo de Contacto 1L', 4790, 5),

-- Equipos de Medición
('Cinta Métrica 5m', 4990, 6),
('Nivel de Burbuja 40cm', 6990, 6),
('Medidor Láser de Distancia 40m', 24990, 6),
('Escuadra Metálica 30cm', 3990, 6);
