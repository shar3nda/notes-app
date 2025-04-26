import { Toaster, toaster } from "@/components/ui/toaster";
import type { NoteRead, NoteUpdate } from "@/types/note";
import {
  Box,
  Button,
  Flex,
  Input,
  Separator,
  Spinner,
  Tag,
  Text,
  Textarea,
  VStack,
} from "@chakra-ui/react";
import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { $api } from "./api";
import { login, register } from "./auth-api";
import { clearTokens, getAccessToken } from "./auth";

function NoteList({
  notes,
  onSelect,
  selectedNoteId,
}: {
  notes: NoteRead[];
  onSelect: (note: NoteRead) => void;
  selectedNoteId: number | null;
}) {
  return (
    <VStack align="stretch" p={2} pt={0} overflowY="auto" w="100%">
      {notes.map((note) => {
        const isSelected = note.id === selectedNoteId;
        return (
          <Box
            key={note.id}
            p={3}
            pb={1}
            borderRadius="md"
            borderWidth={1}
            bg={isSelected ? "bg.emphasized" : "bg"}
            _hover={!isSelected ? { bg: "bg.muted" } : {}}
            cursor="pointer"
            onClick={() => onSelect(note)}
          >
            <Text fontWeight="bold" truncate>
              {note.title || "Untitled"}
            </Text>
            <Text fontSize="sm" lineClamp={1}>
              {note.content || "<No content>"}
            </Text>
            <Tag.Root my={1}>
              <Tag.Label>
                Last modified: {new Date(note.updated_at).toLocaleString()}
              </Tag.Label>
            </Tag.Root>
          </Box>
        );
      })}
    </VStack>
  );
}

function NoteEditor({
  noteId,
  onUpdate,
  onDelete,
}: {
  noteId: NoteRead["id"];
  onUpdate: (id: number, data: NoteUpdate) => void;
  onDelete: (id: number) => void;
}) {
  const { data: note, isLoading } = $api.useQuery("get", "/notes/{note_id}", {
    params: { path: { note_id: noteId } },
  });

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  useEffect(() => {
    if (note) {
      setTitle(note.title);
      setContent(note.content);
    }
  }, [note]);

  if (isLoading || note === undefined) {
    return (
      <Flex flex={1} align="center" justify="center">
        <Spinner size="xl" />
      </Flex>
    );
  }

  return (
    <VStack align="stretch" p={2} flex={1}>
      <Input
        placeholder="Title..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        fontSize="xl"
        fontWeight="bold"
      />
      <Textarea
        placeholder="Your note..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={20}
      />
      <Flex gap={2}>
        <Button onClick={() => onUpdate(note.id, { title, content })}>
          Save
        </Button>
        <Button onClick={() => onDelete(note.id)}>Delete</Button>
      </Flex>
    </VStack>
  );
}

const NotesApp = () => {
  const queryClient = useQueryClient();

  const [selectedNote, setSelectedNote] = useState<NoteRead | null>(null);

  const { data: notes, isLoading } = $api.useQuery("get", "/notes/");
  const { mutate: createNote } = $api.useMutation("post", "/notes/", {
    onSuccess: (newNote: NoteRead) => {
      queryClient.invalidateQueries({ queryKey: ["get", "/notes/"] });
      setSelectedNote(newNote);
    },
  });
  const { mutate: updateNote } = $api.useMutation("put", "/notes/{note_id}", {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["get", "/notes/"] });
      toaster.create({ title: "Note updated", type: "info" });
    },
  });
  const { mutate: deleteNote } = $api.useMutation(
    "delete",
    "/notes/{note_id}",
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ["get", "/notes/"] });
        toaster.create({ title: "Note deleted", type: "info" });
      },
    },
  );

  const handleCreate = () => {
    createNote({ body: { title: "New Note", content: "" } });
  };

  const handleUpdate = (id: number, data: NoteUpdate) => {
    updateNote({ params: { path: { note_id: id } }, body: data });
  };

  const handleDelete = (id: number) => {
    deleteNote({ params: { path: { note_id: id } } });
    setSelectedNote(null);
  };

  const handleLogout = () => {
    clearTokens();
    window.location.reload();
  };

  if (isLoading)
    return (
      <Flex flex={1} align="center" justify="center">
        <Spinner size="xl" />
      </Flex>
    );

  return (
    <VStack w="100%" h="100vh">
      <Flex
        as="nav"
        w="100%"
        px={4}
        pt={2}
        pb={0}
        align="center"
        justify="space-between"
      >
        <Button onClick={handleCreate}>New Note</Button>
        <Button onClick={handleLogout}>Log Out</Button>
      </Flex>

      <Separator orientation="horizontal" w="100%" />

      <Flex w="100%" flex={1} overflow="hidden">
        <VStack w="30%" overflowY="auto">
          {notes && (
            <NoteList
              notes={notes}
              selectedNoteId={selectedNote?.id ?? null}
              onSelect={(note) => setSelectedNote(note)}
            />
          )}
        </VStack>
        {selectedNote?.id ? (
          <NoteEditor
            noteId={selectedNote?.id}
            onUpdate={handleUpdate}
            onDelete={handleDelete}
          />
        ) : (
          <Flex flex={1} align="center" justify="center">
            <Text fontSize="xl" color="gray.500">
              Select a note to view/edit
            </Text>
          </Flex>
        )}
      </Flex>
    </VStack>
  );
};

const App = () => {
  const [loggedIn, setLoggedIn] = useState(!!getAccessToken());
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleAuth = async () => {
    try {
      if (isRegister) {
        await register(username, password);
        toaster.create({ title: "Registered successfully!", type: "success" });
      }
      await login(username, password);
      setLoggedIn(true);
      toaster.create({ title: "Logged in!", type: "success" });
    } catch (err) {
      toaster.create({ title: `Authentication failed: ${err}`, type: "error" });
    }
  };

  if (!loggedIn) {
    return (
      <>
        <Flex
          direction="column"
          p={8}
          gap={4}
          maxW="400px"
          m="auto"
          as="form"
          onSubmit={(e) => {
            e.preventDefault();
            handleAuth();
          }}
        >
          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button onClick={handleAuth} type="submit">
            {isRegister ? "Register" : "Login"}
          </Button>
          <Button
            onClick={() => setIsRegister((r) => !r)}
            variant="outline"
            type="button"
          >
            {isRegister
              ? "Already have an account? Log in"
              : "No account? Register"}
          </Button>
        </Flex>
        <Toaster />
      </>
    );
  }
  return (
    <>
      <Flex h="100vh">
        <NotesApp />
      </Flex>
      <Toaster />
    </>
  );
};

export default App;
