#!/usr/bin/env bun

import {Command} from "commander";
import { runwakeup } from "./tui/wakeup";

const program = new Command();

program
  .name("byteclaw-build")
  .description("A simple CLI tool")
  .version("1.0.0");

program
  .command("wakeup")
  .description("Show the banner and pick cli or telegram mode")
  .action(
    async () => {
      await  runwakeup();
    }
 );



 await program.parseAsync(process.argv);