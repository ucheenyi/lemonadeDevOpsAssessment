# Use official PHP image with Apache
FROM php:8.1-apache

# Install system dependencies and PHP extensions required by Laravel
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zip \
    git \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo pdo_mysql opcache \
    && apt-get clean

# Enable Apache mod_rewrite (required for Laravel's routing)
RUN a2enmod rewrite

# Set the working directory inside the container
WORKDIR /var/www/html

# Copy the existing Laravel app to the container's working directory
COPY . /var/www/html

# Set the correct file permissions for Laravel storage and cache
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Install Composer (PHP dependency manager)
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Install Laravel dependencies via Composer
RUN composer install --no-dev --optimize-autoloader

# Expose port 80 to access the application
EXPOSE 80

# Start Apache in the foreground
CMD ["apache2-foreground"]
