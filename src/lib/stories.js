// Eagerly loads every story JSON under src/data at build time.
// Adding a new story = drop a JSON file in src/data/<level>/stage-<n>/<id>.json
const modules = import.meta.glob('/src/data/*/stage-*/*.json', { eager: true });

export const LEVELS = ['n5', 'n4', 'n3', 'n2', 'n1'];
export const STAGES_PER_LEVEL = 5;

const allStories = Object.values(modules).map((m) => m.default);

export function getStoriesFor(level, stage) {
  return allStories
    .filter((s) => s.level === level && s.stage === Number(stage))
    .sort((a, b) => a.id.localeCompare(b.id));
}

export function getStory(level, stage, id) {
  return allStories.find(
    (s) => s.level === level && s.stage === Number(stage) && s.id === id
  );
}

export function stageHasStories(level, stage) {
  return getStoriesFor(level, stage).length > 0;
}

export function allStoryParams() {
  return allStories.map((s) => ({
    params: { level: s.level, stage: String(s.stage), story: s.id },
  }));
}
