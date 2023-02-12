# Backup System

This project aims to create a backup system that retrieves a zip file from a web server, extracts a SQL dump, verifies its integrity, and creates a new archive in a specified format with a configurable retention period. The new archive is then transferred to a remote server using a chosen transfer method ( FTP ). The system allows the storage of multiple versions of the backup on the destination server with a configurable retention period, and generates logs and email notifications to aid in the monitoring of the backup process.
