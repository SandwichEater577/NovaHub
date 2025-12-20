use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use web_sys::console;
use std::collections::HashMap;
use std::sync::Mutex;
use once_cell::sync::Lazy;

#[derive(Deserialize)]
struct RepoStats {
    stargazers_count: u32,
    forks_count: u32,
    open_issues_count: u32,
}

#[derive(Deserialize)]
struct Contributor {
    login: String,
    avatar_url: String,
    html_url: String,
    contributions: u32,
}

#[wasm_bindgen(start)]
pub async fn main_js() -> Result<(), JsValue> {
    console::log_1(&"🚀 Rust (WASM) initialized for Valyxo Web!".into());
    
    // Fetch and update all data
    let _ = update_stats().await;
    let _ = update_contributors().await;
    let _ = update_languages().await;

    Ok(())
}

async fn update_stats() -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");

    if let Some(el) = document.get_element_by_id("star-count") {
        el.set_text_content(Some("Loading..."));
    }

    if let Ok(resp) = reqwest::get("https://api.github.com/repos/SandwichEater577/Valyxo").await {
        if let Ok(stats) = resp.json::<RepoStats>().await {
            let _ = update_text("star-count", &format!("{} stars", stats.stargazers_count));
            let _ = update_text("fork-count", &format!("{} forks", stats.forks_count));
            let _ = update_text("issue-count", &format!("{} issues", stats.open_issues_count));
        }
    }
    
    Ok(())
}

async fn update_contributors() -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    
    if let Some(container) = document.get_element_by_id("contributors-list") {
       if let Ok(resp) = reqwest::get("https://api.github.com/repos/SandwichEater577/Valyxo/contributors").await {
           if let Ok(contributors) = resp.json::<Vec<Contributor>>().await {
               let filtered: Vec<&Contributor> = contributors.iter()
                   .filter(|c| c.login.to_lowercase() != "michalmazur")
                   .collect();
               
               container.set_inner_html("");
               
               for c in filtered {
                   let a = document.create_element("a")?;
                   a.set_attribute("href", &c.html_url)?;
                   a.set_attribute("target", "_blank")?;
                   a.set_attribute("class", "contributor")?;
                   
                   let img = document.create_element("img")?;
                   img.set_attribute("src", &c.avatar_url)?;
                   img.set_attribute("class", "contributor-avatar-img")?;
                   
                   let span_name = document.create_element("span")?;
                   span_name.set_text_content(Some(&c.login));
                   
                   let span_commits = document.create_element("span")?;
                   span_commits.set_attribute("class", "contributor-commits")?;
                   span_commits.set_text_content(Some(&format!("{} commits", c.contributions)));
                   
                   a.append_child(&img)?;
                   a.append_child(&span_name)?;
                   a.append_child(&span_commits)?;
                   container.append_child(&a)?;
               }
           }
       }
    }
    Ok(())
}

async fn update_languages() -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    
    let colors = get_language_colors();

    if let Ok(resp) = reqwest::get("https://api.github.com/repos/SandwichEater577/Valyxo/languages").await {
        if let Ok(languages) = resp.json::<HashMap<String, u64>>().await {
            let total_bytes: u64 = languages.values().sum();
            
            if let Some(bar) = document.get_element_by_id("language-bar") {
                bar.set_inner_html("");
                if let Some(list) = document.get_element_by_id("language-list") {
                    list.set_inner_html("");
                    
                    let mut sorted_langs: Vec<_> = languages.iter().collect();
                    sorted_langs.sort_by(|a, b| b.1.cmp(a.1));

                    for (lang, bytes) in sorted_langs {
                        let percent = (*bytes as f64 / total_bytes as f64) * 100.0;
                        if percent < 1.0 { continue; }

                        let color = colors.get(lang).cloned().unwrap_or("#ccc");

                        // Bar segment
                        let segment = document.create_element("div")?;
                        segment.set_attribute("class", "lang-segment")?;
                        let style = format!("width: {:.1}%; background: {}", percent, color);
                        segment.set_attribute("style", &style)?;
                        segment.set_attribute("title", &format!("{}: {:.1}%", lang, percent))?;
                        bar.append_child(&segment)?;

                        // List item
                        let item = document.create_element("div")?;
                        item.set_attribute("class", "lang-item")?;
                        item.set_inner_html(&format!(
                            "<span class=\"lang-dot\" style=\"background: {}\"></span> {} <span class=\"lang-percent\">{:.1}%</span>",
                            color, lang, percent
                        ));
                        list.append_child(&item)?;
                    }
                }
            }
        }
    }
    Ok(())
}

fn update_text(id: &str, text: &str) -> Result<(), JsValue> {
    let window = web_sys::window().expect("no global `window` exists");
    let document = window.document().expect("should have a document on window");
    if let Some(el) = document.get_element_by_id(id) {
        el.set_text_content(Some(text));
    }
    Ok(())
}


// --- Terminal Logic (Rustified) ---

#[derive(Clone, Serialize, Deserialize)]
pub enum FSNode {
    File { content: String },
    Directory { children: HashMap<String, FSNode> },
}

pub struct VirtualFileSystem {
    root: FSNode,
}

impl VirtualFileSystem {
    pub fn new() -> Self {
        let mut root_children = HashMap::new();
        
        // Projects folder
        let mut projects_children = HashMap::new();
        projects_children.insert("hello.ns".to_string(), FSNode::File { 
            content: "// ValyxoScript Example\nprint \"Hello from Rust WASM!\"\nlet x = 42\nprint x".to_string() 
        });
        projects_children.insert("readme.txt".to_string(), FSNode::File { 
            content: "Valyxo Terminal (Rust Edition)\n\nThis entire filesystem is running in Rust!".to_string() 
        });
        root_children.insert("projects".to_string(), FSNode::Directory { children: projects_children });
        
        // Docs folder
        let mut docs_children = HashMap::new();
        docs_children.insert("manifesto.txt".to_string(), FSNode::File { 
            content: "Speed. Safety. Rust.".to_string() 
        });
        root_children.insert("docs".to_string(), FSNode::Directory { children: docs_children });

        Self {
            root: FSNode::Directory { children: root_children },
        }
    }

    pub fn get_node(&self, path: &str) -> Option<&FSNode> {
        let mut current = &self.root;
        for part in path.split('/').filter(|s| !s.is_empty()) {
            match current {
                FSNode::Directory { children } => {
                    current = children.get(part)?;
                }
                _ => return None,
            }
        }
        Some(current)
    }

    pub fn get_node_mut(&mut self, path: &str) -> Option<&mut FSNode> {
        let mut current = &mut self.root;
        for part in path.split('/').filter(|s| !s.is_empty()) {
            match current {
                FSNode::Directory { children } => {
                    current = children.get_mut(part)?;
                }
                _ => return None,
            }
        }
        Some(current)
    }
}

pub struct TerminalSession {
    vfs: VirtualFileSystem,
    cwd: String,
    history: Vec<String>,
}

impl TerminalSession {
    pub fn new() -> Self {
        Self {
            vfs: VirtualFileSystem::new(),
            cwd: "/".to_string(),
            history: Vec::new(),
        }
    }

    pub fn execute(&mut self, input: String) -> String {
        let trimmed = input.trim();
        if trimmed.is_empty() { return String::new(); }
        
        self.history.push(trimmed.to_string());
        let parts: Vec<&str> = trimmed.split_whitespace().collect();
        let cmd = parts[0].to_lowercase();
        let args = if parts.len() > 1 { parts[1..].join(" ") } else { String::new() };

        match cmd.as_str() {
            "ls" => self.ls(&args),
            "cd" => self.cd(&args),
            "cat" => self.cat(&args),
            "echo" => self.echo(&args),
            "clear" => "CLEAR_COMMAND".to_string(),
            "-help" => self.help(),
            "man" => self.man(&args),
            _ => format!("Command not found: {}. Type '-help' for available commands.", cmd),
        }
    }

    fn ls(&self, args: &str) -> String {
        let path = if args.is_empty() { self.cwd.clone() } else { self.resolve_path(args) };
        match self.vfs.get_node(&path) {
            Some(FSNode::Directory { children }) => {
                let mut names: Vec<_> = children.iter().map(|(k, v)| {
                    let prefix = match v { FSNode::Directory { .. } => "📁 ", _ => "📄 " };
                    format!("  {}{}", prefix, k)
                }).collect();
                names.sort();
                if names.is_empty() { "(empty directory)".to_string() } else { names.join("\n") }
            }
            Some(_) => format!("ls: {}: Not a directory", args),
            None => format!("ls: {}: No such directory", args),
        }
    }

    fn cd(&mut self, args: &str) -> String {
        if args.is_empty() { 
            self.cwd = "/".to_string(); 
            return "Changed to: /".to_string();
        }
        let new_path = self.resolve_path(args);
        match self.vfs.get_node(&new_path) {
            Some(FSNode::Directory { .. }) => {
                self.cwd = new_path;
                format!("Changed to: {}", self.cwd)
            }
            _ => format!("cd: no such directory: {}", args),
        }
    }

    fn cat(&self, args: &str) -> String {
        if args.is_empty() { return "Usage: cat <file>".to_string(); }
        let path = self.resolve_path(args);
        match self.vfs.get_node(&path) {
            Some(FSNode::File { content }) => content.clone(),
            Some(FSNode::Directory { .. }) => format!("cat: {}: Is a directory", args),
            None => format!("cat: {}: No such file", args),
        }
    }

    fn echo(&mut self, args: &str) -> String {
        if args.contains('>') {
            let parts: Vec<&str> = args.splitn(2, '>').collect();
            let text = parts[0].trim().trim_matches('"');
            let filename = parts[1].trim();
            
            let path = self.resolve_path(filename);
            let mut parent_path = path.clone();
            if let Some(idx) = parent_path.rfind('/') {
                parent_path.truncate(idx + 1);
            }
            
            // This is a simplified implementation for demo
            if let Some(FSNode::Directory { children }) = self.vfs.get_node_mut(&parent_path) {
                let name = filename.rsplit('/').next().unwrap();
                children.insert(name.to_string(), FSNode::File { content: text.to_string() });
                return format!("Written to {}", filename);
            }
        }
        args.to_string()
    }

    fn help(&self) -> String {
        "╭─ Valyxo v0.6.0 Rust Core ────────────────────────────╮\n\
         │                                                     │\n\
         │  Commands: ls, cd, cat, echo, clear, man, -help     │\n\
         │  Type 'man valyxo' for overview                     │\n\
         │                                                     │\n\
         │  (Virtual Filesystem running in Rust WASM)          │\n\
         ╰─────────────────────────────────────────────────────╯".to_string()
    }

    fn man(&self, cmd: &str) -> String {
        match cmd {
            "valyxo" => "VALYXO(1) - The Fast Developer Platform\n\nRust-powered online terminal demo.".to_string(),
            "echo" => "ECHO(1) - Display text or write to file\n\nUsage: echo \"text\" > file.txt".to_string(),
            _ => format!("No manual entry for {}", cmd),
        }
    }

    fn resolve_path(&self, path: &str) -> String {
        if path.starts_with('/') { return path.to_string(); }
        if path == ".." {
             let mut parts: Vec<&str> = self.cwd.split('/').filter(|s| !s.is_empty()).collect();
             parts.pop();
             return format!("/{}", parts.join("/"));
        }
        if self.cwd == "/" { format!("/{}", path) }
        else { format!("{}/{}", self.cwd, path) }
    }
}

static SESSION: Lazy<Mutex<TerminalSession>> = Lazy::new(|| Mutex::new(TerminalSession::new()));

#[wasm_bindgen]
pub fn terminal_input(input: String) -> String {
    let mut session = SESSION.lock().unwrap();
    session.execute(input)
}

#[wasm_bindgen]
pub fn get_cwd() -> String {
    let session = SESSION.lock().unwrap();
    session.cwd.clone()
}
