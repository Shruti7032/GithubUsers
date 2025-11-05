#!/usr/bin/env node
/**
 * Catholic Daily Readings Fetcher (Node.js)
 * 
 * Uses the get-catholic-daily-readings npm package to fetch readings
 * for November 2025 - December 2026
 * 
 * Installation:
 *   npm install get-catholic-daily-readings
 * 
 * Usage:
 *   node fetch_readings_nodejs.js
 */

const fs = require('fs');
const path = require('path');

// Try to import the package
let getCatholicReadings;
try {
    getCatholicReadings = require('get-catholic-daily-readings');
} catch (error) {
    console.error('Error: get-catholic-daily-readings package not installed.');
    console.error('Please run: npm install get-catholic-daily-readings');
    process.exit(1);
}

// Helper to add days to a date
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

// Helper to format date as YYYY-MM-DD
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Helper to format date for the package (MM-DD-YYYY)
function formatDateForPackage(date) {
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const year = date.getFullYear();
    return `${month}-${day}-${year}`;
}

// Helper to add delay
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchReadingForDate(date) {
    const dateStr = formatDate(date);
    const packageDateStr = formatDateForPackage(date);
    
    try {
        console.log(`Fetching readings for ${dateStr}...`);
        
        // The package expects date in MM-DD-YYYY format
        const data = await getCatholicReadings(packageDateStr);
        
        if (!data) {
            console.log(`  ⚠ No data returned for ${dateStr}`);
            return createPlaceholder(dateStr);
        }
        
        // Parse the response
        const reading = {
            date: dateStr,
            title: data.title || data.name || `Daily Reading - ${date.toLocaleDateString('en-US', { weekday: 'long' })}`,
            readings: []
        };
        
        // Extract readings from the data structure
        // The package structure varies, so we need to handle different formats
        if (data.readings) {
            for (const r of data.readings) {
                reading.readings.push({
                    type: r.type || r.label || 'Reading',
                    citation: r.citation || r.reference || '',
                    text: r.text || r.content || ''
                });
            }
        } else if (data.reading1 || data.gospel) {
            // Alternative structure
            if (data.reading1) {
                reading.readings.push({
                    type: 'First Reading',
                    citation: data.reading1.citation || '',
                    text: data.reading1.content || ''
                });
            }
            if (data.psalm) {
                reading.readings.push({
                    type: 'Psalm',
                    citation: data.psalm.citation || '',
                    text: data.psalm.content || ''
                });
            }
            if (data.reading2) {
                reading.readings.push({
                    type: 'Second Reading',
                    citation: data.reading2.citation || '',
                    text: data.reading2.content || ''
                });
            }
            if (data.gospel) {
                reading.readings.push({
                    type: 'Gospel',
                    citation: data.gospel.citation || '',
                    text: data.gospel.content || ''
                });
            }
        }
        
        // If no readings found, create placeholder
        if (reading.readings.length === 0) {
            console.log(`  ⚠ No readings data for ${dateStr}`);
            return createPlaceholder(dateStr, reading.title);
        }
        
        console.log(`  ✓ Successfully fetched ${reading.readings.length} readings`);
        return reading;
        
    } catch (error) {
        console.error(`  ✗ Error fetching ${dateStr}: ${error.message}`);
        return createPlaceholder(dateStr);
    }
}

function createPlaceholder(dateStr, title = null) {
    const date = new Date(dateStr);
    const defaultTitle = title || `Daily Reading - ${date.toLocaleDateString('en-US', { weekday: 'long' })}`;
    
    return {
        date: dateStr,
        title: defaultTitle,
        readings: [
            {
                type: 'First Reading',
                citation: 'Data not yet available',
                text: `Reading data for ${dateStr} will be available when published by liturgical sources.`
            },
            {
                type: 'Psalm',
                citation: 'Data not yet available',
                text: `Psalm for ${dateStr} will be available when published.`
            },
            {
                type: 'Gospel',
                citation: 'Data not yet available',
                text: `Gospel reading for ${dateStr} will be available when published.`
            }
        ]
    };
}

async function fetchAllReadings() {
    console.log('=' .repeat(70));
    console.log('Catholic Daily Readings Fetcher (Node.js)');
    console.log('Using: get-catholic-daily-readings package');
    console.log('=' .repeat(70));
    console.log();
    
    const startDate = new Date('2025-11-01');
    const endDate = new Date('2026-12-31');
    const readings = [];
    
    let currentDate = new Date(startDate);
    let dayCount = 0;
    const totalDays = Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
    
    console.log(`Fetching readings from ${formatDate(startDate)} to ${formatDate(endDate)}`);
    console.log(`Total days: ${totalDays}`);
    console.log();
    
    while (currentDate <= endDate) {
        dayCount++;
        
        if (dayCount % 10 === 0 || dayCount === 1) {
            console.log(`Progress: ${dayCount}/${totalDays} days processed`);
        }
        
        const reading = await fetchReadingForDate(currentDate);
        readings.push(reading);
        
        // Add delay to be respectful to any underlying APIs
        await delay(200);
        
        currentDate = addDays(currentDate, 1);
    }
    
    console.log();
    console.log(`Completed! Fetched ${readings.length} daily readings.`);
    
    return readings;
}

async function main() {
    try {
        // Fetch all readings
        const readings = await fetchAllReadings();
        
        // Save to JSON file
        const outputPath = path.join(__dirname, 'GithubUsers', 'app', 'src', 'main', 'assets', 'catholic_readings_2026.json');
        
        // Ensure directory exists
        const outputDir = path.dirname(outputPath);
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }
        
        fs.writeFileSync(outputPath, JSON.stringify(readings, null, 2), 'utf8');
        
        const fileSize = fs.statSync(outputPath).size;
        console.log();
        console.log('=' .repeat(70));
        console.log(`JSON file saved to: ${outputPath}`);
        console.log(`File size: ${fileSize.toLocaleString()} bytes (${(fileSize / 1024).toFixed(1)} KB)`);
        console.log();
        
        // Count readings with actual data vs placeholders
        const actualReadings = readings.filter(r => 
            !r.readings[0].text.includes('will be available')
        ).length;
        
        console.log('SUMMARY:');
        console.log('-' .repeat(70));
        console.log(`Total entries: ${readings.length}`);
        console.log(`Entries with actual readings: ${actualReadings}`);
        console.log(`Entries with placeholders: ${readings.length - actualReadings}`);
        console.log(`Date range: ${readings[0].date} to ${readings[readings.length - 1].date}`);
        console.log();
        console.log('✓ File ready for Android app!');
        console.log('=' .repeat(70));
        
    } catch (error) {
        console.error('Fatal error:', error);
        process.exit(1);
    }
}

// Run the script
main();
