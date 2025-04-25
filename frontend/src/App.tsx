import { Toaster, toaster } from "@/components/ui/toaster";
import type { NoteRead, NoteUpdate } from "@/types/note";
import {
  Box,
  Button,
  Flex,
  Input,
  Separator,
  Spinner,
  Text,
  Textarea,
  VStack,
} from "@chakra-ui/react";
import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { $api } from "./api";

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
    <VStack align="stretch" p={2} overflowY="auto" w="100%">
      {notes.map((note) => {
        const isSelected = note.id === selectedNoteId;
        return (
          <Box
            key={note.id}
            p={3}
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
              {note.content || "No content"}
            </Text>
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

const App = () => {
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
    onSuccess: () => toaster.create({ title: "Note updated", type: "info" }),
  });
  const { mutate: deleteNote } = $api.useMutation(
    "delete",
    "/notes/{note_id}",
    {
      onSuccess: () => toaster.create({ title: "Note deleted", type: "info" }),
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

  if (isLoading) return <Spinner size="xl" />;

  return (
    <>
      <Flex h="100vh">
        <VStack w="30%">
          <Button onClick={handleCreate}>New Note</Button>
          {notes && (
            <NoteList
              notes={notes}
              selectedNoteId={selectedNote?.id ?? null}
              onSelect={(note) => setSelectedNote(note)}
            />
          )}
        </VStack>
        <Separator orientation="vertical" />
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
      <Toaster />
    </>
  );
};

export default App;
