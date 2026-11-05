package main

import "core:fmt"
import "core:os"
import "core:strconv"
import "core:strings"

main :: proc() {
	// provide the target file path (Linux)
	mem_path := "/proc/meminfo"

	// read the entire file using std context alloc (Odin's version of malloc)
	mem_data, err := os.read_entire_file(mem_path, context.allocator)
	if err != nil {
		fmt.eprintfln("Error reading file: %v", err)
		return
	}
	// clean up the allocated mem when exiting
	defer delete(mem_data, context.allocator)

	// convert the bytes to a string so we can manipulate or print it
	mem_content := string(mem_data)

	fmt.println("----Mem Info----")
	// loop to find MemTotal:
	/*
	* this loops thru the given string till it reaches a new line char and
	* puts that content inside the line variable we declared
	*/
	for line in strings.split_lines_iterator(&mem_content) {
		if strings.has_prefix(line, "MemTotal:") {
			fmt.println(line)
		}
	}
	fmt.println("           ")

	// call the cpu one
	fmt.println("----CPU Info------")
	cpu_path := "/proc/stat"
	cpu_result, ok := read_cpu(cpu_path)
	// if the read fails..exit early
	if !ok {
		return
	}
	fmt.println(cpu_result)
}

read_cpu :: proc(filepath: string) -> (int, bool) {
	cpu_data, err := os.read_entire_file(filepath, context.allocator)
	if err != nil {
		fmt.eprintfln("Error reading file: %v", err)
		return 0, false
	}
	defer delete(cpu_data, context.allocator)

	// convert to a string
	cpu_content := string(cpu_data)

	// print words starting with "cpu"
	for line in strings.split_lines_iterator(&cpu_content) {
		if strings.has_prefix(line, "cpu") {
			// split the fields
			cpu_fields := strings.fields(line)
			defer delete(cpu_fields)
			// error checking
			if len(cpu_fields) < 2 {
				fmt.println("Something ain't right with your CPU fields bro")
				return 0, false
			}
			return strconv.parse_int(cpu_fields[1])
		}
	}
	// if no line started with "cpu"...
	return 0, false
}
