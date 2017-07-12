import argparse
import pickle
import os

ENTITY_FILENAME = 'entity2id.txt'
RELATION_FILENAME = 'relation2id.txt'
TEST_FILENAME = 'test.txt'
TRAIN_FILENAME = 'train.txt'
VALID_FILENAME = 'valid.txt'

# The input data has a mapping of longform id to short id.
# The short id is actually just an index (starting at 0 and counting up without holes).
# The HolE format does not directly list the id, however it does translate the longform ids into
# the short ids for triples.
# So, we will need to collect the longform ids in order AND build
# a mapping of {longformId: shortId}.
def readMapping(path):
    ids = []
    idMapping = {}

    with open(path, 'r') as inFile:
        for line in inFile:
            longId, shortId = line.strip().split("\t")
            ids.append(longId)
            idMapping[longId] = shortId

    return ids, idMapping

# Triple files are tab separated and are of the form: head, tail, relation.
# The HolE format has the same pattern, but uses a tuple.
# We will need to convert the ids (all are longform in the input data)
# into the short ids (and then to ints) using the provided mappings.
def readTriples(path, entityIdMapping, relationIdMapping):
    triples = []

    with open(path, 'r') as inFile:
        for line in inFile:
            triple = line.strip().split("\t")
            triples.append((
                int(entityIdMapping[triple[0]]),
                int(entityIdMapping[triple[1]]),
                int(relationIdMapping[triple[2]])
            ))

    return triples

def readData(inDir):
    # All the data to be pickled.
    data = {}

    data['entities'], entityIdMapping = readMapping(os.path.join(inDir, ENTITY_FILENAME))
    data['relations'], relationIdMapping = readMapping(os.path.join(inDir, RELATION_FILENAME))

    data['test_subs'] = readTriples(os.path.join(inDir, TEST_FILENAME), entityIdMapping, relationIdMapping)
    data['train_subs'] = readTriples(os.path.join(inDir, TRAIN_FILENAME), entityIdMapping, relationIdMapping)
    data['valid_subs'] = readTriples(os.path.join(inDir, VALID_FILENAME), entityIdMapping, relationIdMapping)

    return data

def parseArgs():
    parser = argparse.ArgumentParser(description = 'Convert data from the format specified in (https://github.com/thunlp/KB2E) into the HolE pickle.')
    parser.add_argument('--inDir', type = str, help = 'the input data dir', required = True)
    parser.add_argument('--out', type = str, help = 'the output path for the pickle', required = True)

    args = parser.parse_args()

    return args.inDir, args.out

def main():
    inDir, outPath = parseArgs()

    data = readData(inDir)

    with open(outPath, 'wb') as outFile:
        pickle.dump(data, outFile, protocol = pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main()
