const unzipper = require('unzipper');
const fs = require('fs');
const path = require('path');
const PDFDocument = require('pdfkit');
const sizeOf = require('image-size');
console.log(`Recibido: ZIP = ${process.argv[2]}, Serie = ${process.argv[3]}, Capítulo = ${process.argv[4]}`);


// Función para extraer el ZIP a un directorio temporal
async function extractZip(zipPath, extractTo) {
    return fs.createReadStream(zipPath)
        .pipe(unzipper.Extract({ path: extractTo }))
        .promise();
}

// Función para obtener todos los archivos de imagen en un directorio
function getImageFiles(directory) {
    return fs.readdirSync(directory, { withFileTypes: true })
        .filter(dirent => dirent.isFile())
        .filter(file => {
            const ext = path.extname(file.name).toLowerCase();
            return ext === '.jpg' || ext === '.jpeg' || ext === '.png';
        })
        .map(file => path.join(directory, file.name));
}

// Función para obtener las subcarpetas dentro de un directorio
function getDirectories(source) {
    return fs.readdirSync(source, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => path.join(source, dirent.name));
}

// Función para convertir imágenes en PDF usando PDFKit
function imagesToPDF(imagePaths, outputPDFPath) {
    return new Promise((resolve, reject) => {
        const doc = new PDFDocument({ autoFirstPage: false }); // Desactivar la primera página automática
        const stream = fs.createWriteStream(outputPDFPath);
        doc.pipe(stream);

        imagePaths.forEach(imagePath => {
            const dimensions = sizeOf(imagePath); // Obtener las dimensiones de la imagen

            // Crear una nueva página con las mismas dimensiones que la imagen
            doc.addPage({ size: [dimensions.width, dimensions.height] });

            // Insertar la imagen en la página sin modificar su tamaño
            doc.image(imagePath, 0, 0, { width: dimensions.width, height: dimensions.height });
        });

        doc.end();

        stream.on('finish', () => {
            resolve(outputPDFPath);
        });

        stream.on('error', reject);
    });
}

// Función para procesar un solo archivo ZIP y generar los PDFs
async function processSingleZip(zipFilePath, outputDir, serie, chapter) {
    const tempDir = './temp_extracted_' + path.basename(zipFilePath, '.zip'); // Carpeta temporal para cada ZIP
    await extractZip(zipFilePath, tempDir);

    const directories = getDirectories(tempDir); // Obtener todas las subcarpetas

    if (directories.length === 0) {
        // Si no hay subcarpetas, procesa las imágenes en la raíz
        const images = getImageFiles(tempDir);
        if (images.length > 0) {
            const outputPDFPath = path.join(outputDir, `${serie}_${chapter}.pdf`);
            await imagesToPDF(images, outputPDFPath);
            console.log(`PDF creado en ${outputPDFPath}`);
        } else {
            console.log(`No se encontraron imágenes en el ZIP: ${zipFilePath}`);
        }
    } else {
        // Procesa las imágenes dentro de cada subcarpeta
        for (const directory of directories) {
            const images = getImageFiles(directory); // Obtener imágenes dentro de cada carpeta

            if (images.length === 0) {
                console.log(`No se encontraron imágenes en la carpeta: ${directory}`);
                continue;
            }

            const folderName = path.basename(directory);
            const outputPDFPath = path.join(outputDir, `${serie}_${chapter}_${folderName}.pdf`);

            await imagesToPDF(images, outputPDFPath); // Crear el PDF con las imágenes

            console.log(`PDF creado para la carpeta ${folderName} en ${outputPDFPath}`);
        }
    }

    // Eliminar los archivos temporales
    fs.rmSync(tempDir, { recursive: true, force: true });
}

// Función para procesar todos los ZIPs en la carpeta "temp" y generar los PDFs en "output_pdfs"
async function processZipsInTempFolder(serie, chapter) {
    const zipFolderPath = path.join(__dirname, '../temp'); // Carpeta "temp" donde se descargan los ZIPs
    const outputDirectory = path.join(zipFolderPath, 'output_pdfs'); // Carpeta de salida para los PDFs

    // Crear la carpeta de salida si no existe
    if (!fs.existsSync(outputDirectory)) {
        fs.mkdirSync(outputDirectory);
    }

    const zipFiles = fs.readdirSync(zipFolderPath).filter(file => path.extname(file) === '.zip');
    
    if (zipFiles.length === 0) {
        console.log(`No se encontraron archivos ZIP en la carpeta "temp".`);
        return;
    }

    for (const zipFile of zipFiles) {
        const zipFilePath = path.join(zipFolderPath, zipFile);
        await processSingleZip(zipFilePath, outputDirectory, serie, chapter);

        // Después de procesar, eliminar el ZIP
        fs.unlinkSync(zipFilePath);
    }

    console.log('Todos los ZIPs han sido procesados.');
}

// Obtener los argumentos de la línea de comandos (serie y chapter)
const zipFilePath = process.argv[2]; // Ruta del archivo ZIP
const serie = process.argv[3];       // Nombre de la serie
const chapter = process.argv[4];     // Número del capítulo

processZipsInTempFolder(serie, chapter)
    .catch(err => console.error('Error:', err));
