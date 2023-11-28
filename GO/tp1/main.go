package main

import (
	"fmt"
	"os"
)

func main() {
	var argsWithoutProg = os.Args[1:]

	fmt.Println("We have ", len(argsWithoutProg), " arguments:")
	for i, arg := range argsWithoutProg {
		fmt.Println("\t-Arg ", i, " is ", arg)
	}
}
