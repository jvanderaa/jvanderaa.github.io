package main

import (
	"flag"
	"fmt"

	"os"
	"path/filepath"
	"regexp"
	"strings"
)

func main() {
	flag.Parse()
	searchDir := "docs/posts"
	if flag.NArg() > 0 {
		searchDir = flag.Arg(0)
	}

	fmt.Printf("Scanning directory: %s\n", searchDir)

	files, err := getMarkdownFiles(searchDir)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error getting files: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Found %d markdown files.\n", len(files))

	var failures []string

	for _, file := range files {
		passed, count, err := checkFile(file)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error checking file %s: %v\n", file, err)
			continue
		}
		if !passed {
			failures = append(failures, fmt.Sprintf("- %s (Paragraphs: %d)", file, count))
		}
	}

	if len(failures) > 0 {
		fmt.Printf("\nERROR: The following files have more than 2 paragraphs but are missing the '<!-- more -->' tag:\n\n")
		for _, failure := range failures {
			fmt.Println(failure)
		}
		fmt.Println("\nPlease add '<!-- more -->' to these posts to define the summary break.")
		os.Exit(1)
	} else {
		fmt.Println("\nAll files passed the check!")
		os.Exit(0)
	}
}

func getMarkdownFiles(rootDir string) ([]string, error) {
	var markdownFiles []string
	err := filepath.Walk(rootDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() && strings.HasSuffix(info.Name(), ".md") {
			markdownFiles = append(markdownFiles, path)
		}
		return nil
	})
	return markdownFiles, err
}

func checkFile(filePath string) (bool, int, error) {
	contentBytes, err := os.ReadFile(filePath)
	if err != nil {
		return false, 0, err
	}
	content := string(contentBytes)

	// 1. Extract content after frontmatter
	// Regex matches: start of string, ---, newline, anything (lazy), newline, ---, newline, whatever follows
	re := regexp.MustCompile(`(?s)^---\n(.*?)\n---\n(.*)`)
	match := re.FindStringSubmatch(content)

	var body string
	if len(match) >= 3 {
		body = match[2]
	} else {
		// No frontmatter found, use whole content
		body = content
	}

	// 2. Check for <!-- more -->
	if strings.Contains(body, "<!-- more -->") {
		return true, 0, nil
	}

	// 3. Count paragraphs
	// Splitting by standard markdown paragraph separator (at least one empty line between blocks)
	// Python script used re.split(r'\n\s*\n', body.strip())
	// Let's approximate that in Go.

	// Trim leading/trailing whitespace
	body = strings.TrimSpace(body)
	if body == "" {
		return true, 0, nil
	}

	// Split by double newlines (possibly with spaces in between)
	paragraphSplitter := regexp.MustCompile(`\n\s*\n`)
	blocks := paragraphSplitter.Split(body, -1)

	var paragraphs []string
	for _, b := range blocks {
		if strings.TrimSpace(b) != "" {
			paragraphs = append(paragraphs, b)
		}
	}

	count := len(paragraphs)
	if count > 2 {
		return false, count, nil
	}

	return true, count, nil
}
